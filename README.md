<!-- GitHub Profile README — github.com/boxpkaka -->

<p align="center">
  <img src="assets/banner-dark.svg#gh-dark-mode-only" alt="Boxpkaka — speech recognition, from model to device: ASR, SpeechLLM, on-device inference" width="830" />
  <img src="assets/banner-light.svg#gh-light-mode-only" alt="Boxpkaka — speech recognition, from model to device: ASR, SpeechLLM, on-device inference" width="830" />
</p>

<p align="center">
  Building speech systems around recognition, evaluation, model serving, and efficient deployment.
</p>

## <img src="assets/icons/target.svg" width="24" height="24" align="absmiddle" alt="" /> Focus

<table>
  <tr>
    <td width="50%" valign="top"><b><img src="assets/icons/mic.svg" width="20" height="20" align="absmiddle" alt="" /> Speech recognition</b><br />Streaming recognition, decoding, and evaluation</td>
    <td width="50%" valign="top"><b><img src="assets/icons/chat.svg" width="20" height="20" align="absmiddle" alt="" /> Speech language models</b><br />Speech-text modeling, instruction tuning, and inference</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><b><img src="assets/icons/speaker.svg" width="20" height="20" align="absmiddle" alt="" /> Speaker-aware recognition</b><br />Target-speaker ASR, speaker diarization, and hotword biasing</td>
    <td width="50%" valign="top"><b><img src="assets/icons/translate.svg" width="20" height="20" align="absmiddle" alt="" /> Simultaneous speech translation</b><br />Streaming speech translation, machine translation, and simultaneous interpretation</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><b><img src="assets/icons/chip.svg" width="20" height="20" align="absmiddle" alt="" /> On-device inference</b><br />Runtime optimization, deployment, and latency control</td>
    <td width="50%" valign="top"><b><img src="assets/icons/database.svg" width="20" height="20" align="absmiddle" alt="" /> Speech data</b><br />Versioned datasets, benchmarks, and processing lineage</td>
  </tr>
</table>

## <img src="assets/icons/compass.svg" width="24" height="24" align="absmiddle" alt="" /> Engineering Notes

- Build measurable pipelines for data preparation, evaluation, and benchmarks
- Version datasets and benchmarks as declarations, so training and evaluation resolve exact data versions
- Keep deployment paths explicit: model export, runtime integration, and service interfaces
- Treat latency, stability, and error analysis as first-class engineering constraints
- Use public experiments to validate system-level assumptions

## <img src="assets/icons/layers.svg" width="24" height="24" align="absmiddle" alt="" /> Stack

**Modeling & Training**

<p>
  <a href="https://github.com/pytorch/pytorch"><img src="https://img.shields.io/badge/PyTorch-24283b?style=for-the-badge&logo=pytorch&logoColor=7aa2f7&labelColor=1a1b27" alt="PyTorch" /></a>
  <a href="https://github.com/huggingface/huggingface_hub"><img src="https://img.shields.io/badge/Hugging%20Face-24283b?style=for-the-badge&logo=huggingface&logoColor=7aa2f7&labelColor=1a1b27" alt="Hugging Face" /></a>
  <a href="https://github.com/huggingface/transformers"><img src="https://img.shields.io/badge/Transformers-24283b?style=for-the-badge&labelColor=1a1b27" alt="Transformers" /></a>
  <a href="https://github.com/microsoft/DeepSpeed"><img src="https://img.shields.io/badge/DeepSpeed-24283b?style=for-the-badge&labelColor=1a1b27" alt="DeepSpeed" /></a>
  <a href="https://github.com/modelscope/ms-swift"><img src="https://img.shields.io/badge/ms--swift-24283b?style=for-the-badge&labelColor=1a1b27" alt="ms-swift" /></a>
  <a href="https://github.com/huggingface/peft"><img src="https://img.shields.io/badge/PEFT%20%2F%20LoRA-24283b?style=for-the-badge&labelColor=1a1b27" alt="PEFT / LoRA" /></a>
</p>

**Inference & Runtime**

<p>
  <a href="https://github.com/vllm-project/vllm"><img src="https://img.shields.io/badge/vLLM-24283b?style=for-the-badge&labelColor=1a1b27" alt="vLLM" /></a>
  <a href="https://github.com/microsoft/onnxruntime"><img src="https://img.shields.io/badge/ONNX%20Runtime-24283b?style=for-the-badge&logo=onnx&logoColor=7aa2f7&labelColor=1a1b27" alt="ONNX Runtime" /></a>
  <a href="https://github.com/boxpkaka/audiollm-server"><img src="https://img.shields.io/badge/C%20%2F%20C%2B%2B%20runtime-24283b?style=for-the-badge&labelColor=1a1b27" alt="C / C++ runtime" /></a>
</p>

**Speech & Audio**

<p>
  <a href="https://github.com/openai/whisper"><img src="https://img.shields.io/badge/Whisper-24283b?style=for-the-badge&labelColor=1a1b27" alt="Whisper" /></a>
  <a href="https://github.com/modelscope/FunASR"><img src="https://img.shields.io/badge/FunASR-24283b?style=for-the-badge&labelColor=1a1b27" alt="FunASR" /></a>
  <a href="https://github.com/wenet-e2e/wenet"><img src="https://img.shields.io/badge/WeNet-24283b?style=for-the-badge&labelColor=1a1b27" alt="WeNet" /></a>
  <a href="https://github.com/k2-fsa/k2"><img src="https://img.shields.io/badge/k2-24283b?style=for-the-badge&labelColor=1a1b27" alt="k2" /></a>
  <a href="https://github.com/k2-fsa/sherpa-onnx"><img src="https://img.shields.io/badge/Sherpa-24283b?style=for-the-badge&labelColor=1a1b27" alt="Sherpa" /></a>
</p>

**Data & Evaluation**

<p>
  <a href="https://github.com/lance-format/lance"><img src="https://img.shields.io/badge/Lance-24283b?style=for-the-badge&labelColor=1a1b27" alt="Lance" /></a>
</p>

**Serving & Tooling**

<p>
  <a href="https://github.com/fastapi/fastapi"><img src="https://img.shields.io/badge/FastAPI-24283b?style=for-the-badge&logo=fastapi&logoColor=7aa2f7&labelColor=1a1b27" alt="FastAPI" /></a>
  <a href="https://github.com/boxpkaka/audiollm-server"><img src="https://img.shields.io/badge/WebSocket-24283b?style=for-the-badge&labelColor=1a1b27" alt="WebSocket" /></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-24283b?style=for-the-badge&labelColor=1a1b27" alt="uv" /></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/Ruff-24283b?style=for-the-badge&labelColor=1a1b27" alt="Ruff" /></a>
</p>

## <img src="assets/icons/chart.svg" width="24" height="24" align="absmiddle" alt="" /> Public Work

Counted from public repositories I own, plus organization repositories I merge pull requests into.

<p align="center">
  <img src="assets/activity-dark.svg#gh-dark-mode-only" alt="Merged pull requests by month" width="830" />
  <img src="assets/activity-light.svg#gh-light-mode-only" alt="Merged pull requests by month" width="830" />
</p>

<p align="center">
  <img src="assets/languages-dark.svg#gh-dark-mode-only" alt="Share of code by language" width="830" />
  <img src="assets/languages-light.svg#gh-light-mode-only" alt="Share of code by language" width="830" />
</p>
