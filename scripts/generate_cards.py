#!/usr/bin/env python3
"""Generate the SVG cards used by the profile README from public GitHub data.

Languages are counted over public repositories I own plus public repositories
I have merged pull requests into (organization repositories included), instead
of the owned-repositories-only view of github-readme-stats.

Standard library only. Set GITHUB_TOKEN to raise the API rate limit.
"""

import argparse
import calendar
import datetime
import json
import math
import os
import pathlib
import urllib.parse
import urllib.request
from collections import Counter

USER = "boxpkaka"
# A repository owned by someone else counts once I have merged this many PRs there.
MIN_MERGED_PRS = 5
# Languages that describe presentation or build glue rather than the code I write.
IGNORED_LANGUAGES = {"Jupyter Notebook", "HTML", "CSS", "Makefile", "Dockerfile", "Roff"}
MAX_LANGUAGES = 7
MAX_MONTHS_SHOWN = 6

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

WIDTH = 830
PAD = 32
FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'

# Fixed language -> colour slot, so a colour follows the language and not its rank.
LANGUAGE_ORDER = ["Python", "Kotlin", "C++", "Shell", "JavaScript", "Swift", "TypeScript", "TeX"]

# Tokyo Night hues stepped into the data-viz lightness band; every slot set below
# passes validate_palette.js (adjacent CVD and normal-vision separation, 3:1 contrast).
THEMES = {
    "dark": {
        "surface": "#1a1b27", "border": "#2f334d", "chip": "#24283b", "chip_border": "#3b4261",
        "primary": "#c0caf5", "secondary": "#a9b1d6", "muted": "#8089b3", "other": "#7a82a6",
        "series": ["#6a91e5", "#d5783d", "#06ab9a", "#be8831", "#df619a", "#76a440", "#a07fda", "#e3647d"],
        "banner": ("#1a1b27", "#24283b"), "wave": ("#7aa2f7", "#bb9af7"),
    },
    "light": {
        "surface": "#ffffff", "border": "#d0d7de", "chip": "#eef1fa", "chip_border": "#d0d7e8",
        "primary": "#1f2335", "secondary": "#444b6a", "muted": "#6a7090", "other": "#8a90a8",
        "series": ["#4c71c1", "#b25816", "#008779", "#9c6900", "#bb407a", "#58841a", "#8160b7", "#be435e"],
        "banner": ("#ffffff", "#e9ecf5"), "wave": ("#4c71c1", "#8160b7"),
    },
}


def api(path, **params):
    url = "https://api.github.com" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-cards"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def merged_pull_requests():
    """Merged PR counts per repository and per month, over public repositories only."""
    counts = Counter()
    months = Counter()
    for page in range(1, 11):  # the search API stops at 1000 results
        result = api(
            "/search/issues",
            q=f"author:{USER} is:pr is:merged is:public",
            per_page=100,
            page=page,
        )
        for item in result["items"]:
            counts[item["repository_url"].split("/repos/", 1)[1]] += 1
            months[item["pull_request"]["merged_at"][:7]] += 1
        if len(result["items"]) < 100:
            break
    return counts, months


def collect():
    owned = [
        repo["full_name"]
        for repo in api(f"/users/{USER}/repos", per_page=100, type="owner")
        if not repo["fork"] and not repo["archived"] and repo["name"] != USER
    ]
    merged, months = merged_pull_requests()
    contributed = [
        name
        for name, count in merged.items()
        if count >= MIN_MERGED_PRS and not name.lower().startswith(f"{USER.lower()}/")
    ]

    # A personal copy of an organization repository would count the same code twice.
    unique = {}
    for name in contributed + owned:
        unique.setdefault(name.split("/", 1)[1].lower(), name)

    languages = Counter()
    for name in unique.values():
        languages.update(api(f"/repos/{name}/languages"))

    return {
        "generated": datetime.date.today().isoformat(),
        "repos": len(unique),
        "languages": dict(languages),
        "merged_total": sum(months.values()),
        "merged_by_month": dict(months),
    }


def language_rows(languages):
    sizes = {name: size for name, size in languages.items() if name not in IGNORED_LANGUAGES}
    total = sum(sizes.values())
    ranked = sorted(sizes.items(), key=lambda item: -item[1])
    rows = [(name, size / total) for name, size in ranked[:MAX_LANGUAGES]]
    rest = sum(size for _, size in ranked[MAX_LANGUAGES:])
    if rest:
        rows.append(("Other", rest / total))
    return rows


def language_slots(names):
    slots = {name: LANGUAGE_ORDER.index(name) for name in names if name in LANGUAGE_ORDER}
    free = iter(i for i in range(len(LANGUAGE_ORDER)) if i not in slots.values())
    for name in names:
        if name not in slots and name != "Other":
            slots[name] = next(free)
    return slots


def percent(share):
    return "&lt;0.1%" if share < 0.001 else f"{share * 100:.1f}%"


def svg(height, title, desc, style, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">{desc}</desc>
<style>
text {{ font-family: {FONT}; }}
{style}
</style>
{body}
</svg>
"""


def card(theme, height):
    return (
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" '
        f'fill="{theme["surface"]}" stroke="{theme["border"]}"/>'
    )


def card_text_style(theme):
    return (
        f'.title {{ font-size: 20px; font-weight: 600; fill: {theme["primary"]}; }}\n'
        f'.sub {{ font-size: 14px; fill: {theme["muted"]}; }}\n'
        f'.label {{ font-size: 15px; fill: {theme["primary"]}; }}\n'
        f'.value {{ font-size: 15px; font-weight: 600; fill: {theme["primary"]}; }}\n'
        f'.pct {{ font-size: 14px; fill: {theme["muted"]}; }}\n'
        f'.foot {{ font-size: 12px; fill: {theme["muted"]}; }}'
    )


def render_languages(stats, theme):
    rows = language_rows(stats["languages"])
    slots = language_slots([name for name, _ in rows])
    color = lambda name: theme["other"] if name == "Other" else theme["series"][slots[name]]

    gap, bar_y, bar_h, bar_w = 2, 96, 16, WIDTH - 2 * PAD
    usable = bar_w - gap * (len(rows) - 1)
    x = PAD
    segments = []
    for name, share in rows:
        width = max(share * usable, 3)
        segments.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{width:.1f}" height="{bar_h}" fill="{color(name)}"/>')
        x += width + gap

    columns = 4
    column_w = bar_w / columns
    legend = []
    for index, (name, share) in enumerate(rows):
        lx = PAD + (index % columns) * column_w
        ly = 150 + (index // columns) * 34
        legend.append(
            f'<circle cx="{lx + 5:.1f}" cy="{ly - 5}" r="5" fill="{color(name)}"/>'
            f'<text class="label" x="{lx + 20:.1f}" y="{ly}">{name}'
            f'<tspan class="pct" dx="8">{percent(share)}</tspan></text>'
        )

    height = 150 + ((len(rows) - 1) // columns) * 34 + 56
    body = "\n".join(
        [
            card(theme, height),
            '<text class="title" x="32" y="48">Languages</text>',
            f'<text class="sub" x="32" y="72">By code size, across {stats["repos"]} public repositories I own or merge into</text>',
            f'<clipPath id="bar"><rect x="{PAD}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="8"/></clipPath>',
            f'<g clip-path="url(#bar)">{"".join(segments)}</g>',
            *legend,
            f'<text class="foot" x="32" y="{height - 20}">Updated {stats["generated"]}</text>',
        ]
    )
    summary = ", ".join(f"{name} {percent(share)}" for name, share in rows)
    return svg(height, "Languages", f"Share of code by language: {summary}.", card_text_style(theme), body)


def recent_months(stats):
    """Months from the first merged PR up to the current one, newest MAX_MONTHS_SHOWN at most."""
    first = min(stats["merged_by_month"])
    year, month = map(int, stats["generated"].split("-")[:2])
    months = []
    while f"{year:04d}-{month:02d}" >= first and len(months) < MAX_MONTHS_SHOWN:
        months.append(f"{year:04d}-{month:02d}")
        year, month = (year, month - 1) if month > 1 else (year - 1, 12)
    return months[::-1]


def render_activity(stats, theme):
    months = recent_months(stats)
    counts = [stats["merged_by_month"].get(month, 0) for month in months]
    pitch, column_w, radius, baseline, max_h = 80, 24, 4, 214, 100
    first_label = f'{calendar.month_abbr[int(months[0][5:])]} {months[0][:4]}'

    columns = []
    for index, (month, count) in enumerate(zip(months, counts)):
        x = PAD + 16 + index * pitch
        h = max(count / max(counts) * max_h, radius * 2)
        columns.append(
            f'<path d="M{x},{baseline} V{baseline - h + radius:.1f} a{radius},{radius} 0 0 1 {radius},-{radius} '
            f'h{column_w - 2 * radius} a{radius},{radius} 0 0 1 {radius},{radius} V{baseline} z" fill="{theme["series"][0]}"/>'
            f'<text class="value" x="{x + column_w / 2}" y="{baseline - h - 8:.1f}" text-anchor="middle">{count}</text>'
            f'<text class="axis" x="{x + column_w / 2}" y="{baseline + 24}" text-anchor="middle">{calendar.month_abbr[int(month[5:])]}</text>'
        )

    chart_end = PAD + 16 + (len(months) - 1) * pitch + column_w + 16
    stat_x = 590
    height = 296
    body = "\n".join(
        [
            card(theme, height),
            '<text class="title" x="32" y="48">Merged pull requests</text>',
            '<text class="sub" x="32" y="72">By month, public repositories only</text>',
            f'<path d="M{PAD},{baseline + 0.5} H{chart_end}" stroke="{theme["border"]}" stroke-width="1"/>',
            *columns,
            f'<text class="hero" x="{stat_x}" y="152">{stats["merged_total"]}</text>',
            f'<text class="stat" x="{stat_x}" y="180">merged pull requests</text>',
            f'<text class="sub" x="{stat_x}" y="204">since {first_label}</text>',
            f'<text class="foot" x="32" y="{height - 20}">Updated {stats["generated"]}</text>',
        ]
    )
    summary = ", ".join(f"{month} {count}" for month, count in zip(months, counts))
    return svg(
        height, "Merged pull requests",
        f'{stats["merged_total"]} merged pull requests in public repositories since {first_label}. By month: {summary}.',
        card_text_style(theme) + (
            f'\n.axis {{ font-size: 13px; fill: {theme["muted"]}; }}'
            f'\n.hero {{ font-size: 64px; font-weight: 700; fill: {theme["primary"]}; }}'
            f'\n.stat {{ font-size: 16px; fill: {theme["secondary"]}; }}'
        ),
        body,
    )


def render_banner(theme):
    height, baseline = 220, 110
    bars = []
    for i in range(40):
        envelope = 0.5 + 0.5 * math.sin(i * 0.37 + 0.8)
        detail = 0.55 + 0.45 * abs(math.sin(i * 1.3))
        h = 14 + 86 * envelope * detail
        bars.append(
            f'<rect class="bar" style="animation-delay:-{i * 0.11:.2f}s" x="{472 + i * 8.2:.1f}" '
            f'y="{baseline - h / 2:.1f}" width="5" height="{h:.1f}" rx="2.5"/>'
        )

    chips, x = [], 48
    for text in ("ASR", "SpeechLLM", "On-device inference"):
        w = 30 + 8.2 * len(text)
        chips.append(
            f'<rect x="{x:.1f}" y="152" width="{w:.1f}" height="30" rx="15" fill="{theme["chip"]}" stroke="{theme["chip_border"]}"/>'
            f'<text class="chip" x="{x + w / 2:.1f}" y="172" text-anchor="middle">{text}</text>'
        )
        x += w + 10

    start, end = theme["banner"]
    wave_a, wave_b = theme["wave"]
    style = (
        f'.name {{ font-size: 52px; font-weight: 700; fill: {theme["primary"]}; }}\n'
        f'.tag {{ font-size: 18px; fill: {theme["secondary"]}; }}\n'
        f'.chip {{ font-size: 14px; fill: {theme["secondary"]}; }}\n'
        '.bar { fill: url(#wave); transform-box: fill-box; transform-origin: center; animation: pulse 2.6s ease-in-out infinite; }\n'
        '@keyframes pulse { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(0.6); } }\n'
        '@media (prefers-reduced-motion: reduce) { .bar { animation: none; } }'
    )
    body = "\n".join(
        [
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{start}"/><stop offset="1" stop-color="{end}"/></linearGradient>'
            f'<linearGradient id="wave" gradientUnits="userSpaceOnUse" x1="472" y1="0" x2="800" y2="0"><stop offset="0" stop-color="{wave_a}"/><stop offset="1" stop-color="{wave_b}"/></linearGradient></defs>',
            f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="16" fill="url(#bg)" stroke="{theme["border"]}"/>',
            '<text class="name" x="46" y="104">Boxpkaka</text>',
            '<text class="tag" x="48" y="134">Speech recognition, from model to device</text>',
            *chips,
            f'<g aria-hidden="true">{"".join(bars)}</g>',
        ]
    )
    return svg(height, "Boxpkaka", "Speech recognition, from model to device: ASR, SpeechLLM, on-device inference.", style, body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats-only", action="store_true", help="print collected data as JSON and exit")
    parser.add_argument("--stats-file", help="render from a saved --stats-only JSON instead of calling the API")
    args = parser.parse_args()

    if args.stats_file:
        stats = json.loads(pathlib.Path(args.stats_file).read_text())
    else:
        stats = collect()
    if args.stats_only:
        print(json.dumps(stats, indent=1, sort_keys=True))
        return

    ASSETS.mkdir(exist_ok=True)
    for mode, theme in THEMES.items():
        (ASSETS / f"banner-{mode}.svg").write_text(render_banner(theme))
        (ASSETS / f"languages-{mode}.svg").write_text(render_languages(stats, theme))
        (ASSETS / f"activity-{mode}.svg").write_text(render_activity(stats, theme))


if __name__ == "__main__":
    main()
