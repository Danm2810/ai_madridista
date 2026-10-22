# AI Madridista — Architecture & Development Plan

**Status:** Working terminal text chat; standalone local speech experiments

**Version:** 0.1.0

**Last updated:** October 22, 2026

**Development philosophy:** Local-first, modular, incremental, and cost-conscious.

## Project Vision

AI Madridista is a personal football AI character: a passionately biased Real Madrid supporter for casual football banter. The current application runs through the terminal. Voice conversations, persistent memory, optional web search, and additional characters remain future goals.

The character should remain recognizable as roleplay. Its current instructions favor short replies, answering direct questions, and avoiding invented statistics.

## Current Implementation

- Terminal text conversation with Ollama and `gemma4:e4b`.
- Character instructions defined as `SYSTEM_PROMPT` in `characters/madridista.py`.
- In-memory conversation history with a system message and up to 15 completed user/assistant exchanges retained after a successful reply.
- Handling for blank input, `/quit`, end of input, keyboard interruption, connection/model errors, and empty replies.
- Separate Piper and Chatterbox-Turbo speech experiments.
- Root-level application modules and packages; no `src/` or nested `ai_madridista/` package.

The app currently returns complete text replies. It does not stream tokens, synthesize replies, record microphone input, persist conversations, or call external tools.

## Technology and Environments

| Component | Current choice and status |
|---|---|
| Language | Python 3.12; Chatterbox environment uses Python 3.12.10 |
| Interface | Python terminal loop, commonly run in VS Code |
| LLM runtime | Local Ollama server |
| Model | `gemma4:e4b`, installed in `A:\Ollama\models` |
| GPU | NVIDIA RTX 3070, 8 GB VRAM |
| System memory | 32 GB RAM |
| Main application environment | `.venv`; Ollama Python client and Piper |
| Speech experiment environment | `.venv-chatterbox`; Chatterbox-Turbo, Torch 2.6.0+cu124, torchaudio 2.6.0, sounddevice |
| Active speech experiment | Local Chatterbox-Turbo using CUDA and reference audio |
| Earlier speech experiment | Piper with a local ONNX voice |
| Configuration | Python constants in `config.py` |
| Character definition | Python string in `characters/madridista.py` |
| Tests | pytest declared as an optional development dependency; no saved automated tests yet |

The two environments remain separate. Consolidation is deferred until a later compatibility review. VS Code's selected interpreter controls import diagnostics and can differ from the activated terminal environment.

`pyproject.toml` declares the main app's Ollama dependency and optional pytest dependency. Speech experiment dependencies are currently managed separately; the project file does not recreate either complete speech setup.

Chatterbox CUDA generation has worked on the RTX 3070. Simultaneous LLM and speech-model operation still needs memory and latency measurements before integration.

## Current Repository Structure

```text
ai_madridista/                 # Repository root: A:\AI Madridista\ai_madridista
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── pyproject.toml
├── main.py
├── config.py
├── characters/
│   ├── __init__.py
│   └── madridista.py
├── core/
│   ├── __init__.py
│   └── conversation.py
├── providers/
│   ├── __init__.py
│   └── llm/
│       ├── __init__.py
│       └── ollama.py
├── try_chatterbox.py
├── try_piper.py
├── data/                     # Local voice assets and generated audio; ignored
├── .venv/                    # Existing app/Piper environment; ignored
└── .venv-chatterbox/          # Existing Chatterbox environment; ignored
```

Generated caches and packaging metadata are omitted from this diagram. Add future modules when needed rather than creating unused placeholder packages.

## Application Flow and Responsibilities

### Terminal entry point — `main.py`

1. Create a `Conversation` with the character's system instructions.
2. Read and validate terminal input.
3. Append a user message and call `generate_reply()`.
4. Remove the pending user message if generation fails, is interrupted, or returns empty text.
5. Append a successful assistant reply, trim retained history, and display the reply.

`MAX_HISTORY_TURNS = 15` controls retained exchanges. Replies are printed only after generation completes. The terminal layer currently also coordinates the conversation; there is no separate orchestrator module yet.

### Conversation state — `core/conversation.py`

`Conversation` owns the in-memory message list and provides methods to append messages, discard a pending user message, and trim history while preserving the system instructions. Closing the process loses this history.

### LLM adapter — `providers/llm/ollama.py`

`generate_reply(messages)` calls the installed Ollama library's `chat()` function and returns the assistant's text. It reads these values from `config.py`:

- `MODEL = "gemma4:e4b"`
- `NUM_CTX = 4096`
- `NUM_PREDICT = 100`

The request also sets `think=False`. Ollama must be running separately and able to find the configured model. This adapter is a starting point for replaceable providers; provider selection, capability negotiation, streaming, and a formal shared interface are not implemented.

### Character — `characters/madridista.py`

A single Python system-prompt constant defines the current personality. It encourages concise football banter, usually one sentence under 25 words, while allowing longer answers when explicitly requested. JSON character files, character selection, and per-character memory are future work.

## Standalone Speech Experiments

### Chatterbox-Turbo — `try_chatterbox.py`

The current script loads `ChatterboxTurboTTS.from_pretrained(device="cuda")`, generates audio for manually written chunks, and plays audio using `sounddevice`. CUDA synchronization surrounds timing measurements. Playback waits before starting the next generated chunk, allowing the following generation to begin while the current chunk plays.

Reference audio currently points to:

```text
C:\Users\Daniel Mikhail\Downloads\demoman.wav
```

The reference is 13.14 seconds at 44,100 Hz. The voice and Scottish accent have sounded good in local testing; mannerism tuning is deferred. A `LoRACompatibleLinear` deprecation warning has appeared without preventing generation.

**Next agreed step:** Replace manual chunks with automatic splitting of one text string, and test that in this standalone script before connecting AI replies. In the currently saved file, the `text` string is unused and no automatic splitting function is present.

### Piper — `try_piper.py`

The earlier experiment loads `data/voices/en_US-bryce-medium.onnx` with `PiperVoice` and writes a fixed spoken line to `data/piper_test.wav`. It is retained as a separate experiment. Its paths are relative to the terminal's working directory, so run it from the repository root.

Neither script is integrated into the main conversation loop. Speech model loading, playback, and asset paths remain experiment-specific.

## Running the Current Code

From `A:\AI Madridista\ai_madridista` in PowerShell:

```powershell
# Main text chat
& .\.venv\Scripts\python.exe main.py

# Earlier Piper experiment
& .\.venv\Scripts\python.exe try_piper.py

# Current Chatterbox experiment
& .\.venv-chatterbox\Scripts\python.exe try_chatterbox.py
```

Use `python`, not the unavailable Windows `py` launcher. Explicit interpreter paths work even when the terminal has the other environment activated.

Packaging defines the `ai-madridista` command as `main:main`, includes root modules `main` and `config`, and discovers `characters`, `core`, and `providers`. An installed command may require refreshing its editable installation after packaging changes; launching `main.py` directly avoids relying on an older installed entry point.

## Development Roadmap

### Working foundation

Local text chat, a first character prompt, in-memory history, and basic failure handling are implemented. Continue assessing reply quality and performance without treating latency or memory use as fully benchmarked.

### Immediate work — standalone speech

1. Implement automatic text splitting in the Chatterbox experiment.
2. Check sentence boundaries, chunk size, continuity, and playback timing.
3. Measure GPU memory and latency with Ollama and Chatterbox together.
4. Integrate generated AI replies only after the standalone behavior is satisfactory.

### Planned — voice conversations

- Introduce a replaceable local TTS interface and connect the validated speech experiment.
- Add playback interruption and cancellation.
- Add push-to-talk microphone capture and evaluate faster-whisper for transcription.
- Keep microphone recording disabled until push-to-talk is activated.
- Submit transcribed text through the same conversation path as typed input.

These components are planned, not currently implemented. Terminal use remains the priority; a PySide6 desktop interface is tabled.

### Planned — persistent memory and configuration

- Evaluate SQLite for saved conversations and user-approved long-term memories.
- Add restore and deletion controls before relying on persisted data.
- Consider external character/configuration files when needed; JSON and YAML are earlier proposals, not current formats.
- Keep memory responsibilities independent of the model adapter.

### Planned — optional tools and expansion

Optional web search may later provide current football information with clear source attribution. Tool execution, search providers, additional characters, and richer provider interfaces remain future work. No web search or other tool execution is currently connected to the app.

Cloud providers remain an optional future possibility. Current work stays local; paid or cloud speech services should only be revisited at the user's request.

## Engineering and Data Practices

- The user writes important application code, guided through one small actionable step at a time. Housekeeping and explicitly requested fixes can be handled directly.
- Preserve existing work and environments. Review proposed fixes and cleanup before acting when requested.
- Never create Git commits or modify backup branches as part of this workflow.
- Treat synced ChatGPT project sources as read-only references; edit the local working repository.
- Keep secrets, voice recordings, generated audio, private conversations, model files, environments, and generated packaging artifacts out of version control as appropriate. Local application data belongs under `data/`; Ollama models live outside the repository.
- Validate changes with focused checks. Saved automated tests and reproducible speech setup instructions remain useful future maintenance work.

## Definition of Success

The first complete voice-enabled version should support terminal text and push-to-talk conversations with a consistent Madridista personality, local speech generation, and controlled conversation persistence. Optional current-information tools can follow. Core use should remain local and free of recurring API costs.

The current milestone is a working text app plus standalone speech generation. This document distinguishes that implemented state from the goals above and should evolve with the code.
