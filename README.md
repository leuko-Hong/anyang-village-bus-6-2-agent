# Anyang Bus 6-2 Voice Agent

Python voice-query agent scaffold for Anyang village bus route 6-2 (Geumjeong direction).

## Quickstart

```bash
uv run --active python -c "import sys; print(sys.executable)"
uv run --active pytest --collect-only
uv run --active python -m app.cli --audio fixtures/query-geumjeong.wav
```

## Environment

- Required interpreter path: `/Users/leuko/vscode/.venv/bin/python3`
- Dependencies must be installed with `uv`
- Baseline config template: `.env.example`

## Validation Commands

```bash
uv run --active python -c "import sys; print(sys.executable)"
uv run --active basedpyright app
uv run --active pytest -q
uv run --active python -m scripts.run_qa --save-evidence
```

## Runtime Commands

```bash
uv run --active python -m app.cli --audio fixtures/query-geumjeong.wav
uv run --active python -m app.cli --audio fixtures/query-geumjeong.wav --json
uv run --active python -m app.cli --mic
uv run --active python -m app.provider_probe --mode mock
uv run --active python -m app.provider_probe --mode live --base-url http://10.255.255.1
```

## Troubleshooting

- `AUDIO_FILE_NOT_FOUND`: pass a valid `--audio` path.
- `UNSUPPORTED_AUDIO_FORMAT`: use `.wav` input.
- `MIC_DEVICE_UNAVAILABLE`: use `--audio` mode in non-microphone environments.
- `STT_MODEL_UNAVAILABLE`: install `faster-whisper` and rerun STT probe.
- `PROVIDER_TIMEOUT` or `PROVIDER_UNAVAILABLE`: verify API key/base URL and network.
