# AI Madridista — Architecture & Development Plan

**Status:** Planning  
**Version:** 0.1  
**Development philosophy:** Local-first, modular, extensible, and cost-conscious.

## Project Vision

AI Madridista is my personal AI character designed to be an obnoxious, delusional, relentlessly biased Real Madrid supporter (literally any of my friends).

You can argue with the AI through text or voice. The character will defend Real Madrid at every opportunity, make ridiculous football arguments, exaggerate the club's achievements, and find increasingly absurd ways to justify its very dumb opinions.

The underlying application may eventually support additional characters, personalities, AI models, and interaction methods.

## Core Objectives

- Build a program ran through the terminal.
- Support both text conversations and push-to-talk voice interaction.
- Keep microphone recording disabled unless a push-to-talk button is activated.
- Generate spoken responses using text-to-speech.
- Create configurable AI personalities.
- Maintain conversation history and persistent memory.
- Allow optional internet searches for current football information.
- Run locally without recurring API costs.
- Support cloud AI providers through configuration changes.
- Keep components independent and replaceable.
- Make the project suitable for open-source development on GitHub.

## Technology Stack

| Component | Initial Selection |
|---|---|
| Language | Python 3.12 |
| Application framework | lightweight cli module (vscode built-in terminal) |
| Local inference | Ollama |
| Initial LLM | Gemma 4 E4B |
| GPU | NVIDIA RTX 3070, 8 GB VRAM |
| System memory | 32 GB RAM |
| Speech recognition | faster-whisper |
| Speech synthesis | Piper TTS |
| Persistent storage | SQLite |
| Character configuration | JSON |
| Application configuration | YAML |
| Web search | Pluggable search provider |
| Optional cloud models | OpenAI, Anthropic, others |
| Version control | Git / GitHub |
| Testing | pytest |

All technology choices are subject to revision based on performance, experiments and development requirements.

### Hardware considerations

Gemma 4 E4B will be our first candidate, but we will benchmark memory usage and inference speed.

The standard model may exceed available VRAM. We will investigate smaller quantizations and alternative models if necessary.

We should avoid designing around assumptions about model performance before testing on the RTX 3070.

## System Architecture

The application will follow a modular architecture with clearly separated responsibilities.

### Terminal Interface

Responsible for:

- Displaying conversation history.
- Accepting text messages.
- Handling push-to-talk controls.
- Displaying the active character.
- Playing generated speech.
- Showing loading, recording, and response states.
- Providing basic configuration controls.

The interface should not contain model-specific logic.

### Conversation Orchestrator

The central application component.

Responsible for:

- Receiving text or transcribed voice input.
- Loading the selected character's instructions.
- Retrieving relevant conversation history.
- Sending requests to the selected LLM provider.
- Handling tool requests.
- Streaming generated responses.
- Coordinating speech generation.
- Saving conversation history.

### LLM Provider Layer

Provides a common interface for interacting with different models.

Initial implementation:

- Ollama running Gemma 4 locally.

Future implementations:

- OpenAI API.
- Anthropic API.
- Alternative Ollama models.
- Pewdiepie's Ajax to fine-tune the task at hand (locally run)
- Other compatible inference servers.

Provider selection will initially happen through configuration files, not a dedicated settings interface.

Changing providers should not require modifications to the conversation orchestrator.

Provider-specific capabilities, such as tool calling or structured output, will be handled through adapters and capability checks.

### Audio System

Two independent components:

**Speech-to-text**

- Capture microphone audio only while push-to-talk is active.
- Transcribe recorded audio using faster-whisper.
- Submit the transcription as a normal user message.
- Discard temporary recordings by default.

**Text-to-speech**

- Receive generated AI responses.
- Convert text to audio using Piper.
- Play speech through the selected output device.
- Support interruption and cancellation.

Both components will use replaceable provider interfaces to support cloud services later.

### Character Engine

Characters will be defined independently from the underlying model.

Each character can have:

- Name and description.
- System instructions.
- Personality traits.
- Speaking style.
- Voice configuration.
- Behavioral rules.
- Individual conversation history.
- Optional character-specific memory.

The first character will be **AI Madridista**.

Its personality should include:

- Extreme Real Madrid bias.
- Unreasonable confidence.
- Constant football banter.
- Ridiculous justifications for losses.
- Obsessive comparisons with Barcelona.
- Selective interpretation of football statistics.
- Comedic overreactions.
- A refusal to concede arguments easily.

The character may be deliberately delusional or inaccurate for comedic purposes. Its statements should remain recognizable as roleplay rather than authoritative football reporting.

Future characters can be added without modifying the main application.

### Memory System

SQLite will store:

- Conversations.
- Individual messages.
- Character identities.
- Session metadata.
- User-approved long-term memories.

Memory will have two initial levels:

1. **Conversation memory:** Recent messages included in the current conversation.
2. **Persistent memory:** Selected information retained between sessions.

Long-term memory retrieval and automatic summarization can be introduced later.

Memory must remain independent of the selected model.

### Tool System

Tools extend the AI beyond normal text generation.

Initial planned tool:

- Web search for current football news, results, transfers, and statistics.

The orchestrator will manage tool execution independently from the model provider.

Search should be optional, with configurable permissions and a clear distinction between verified information and character-generated opinions.

Future possibilities:

- Football statistics APIs.
- Live match information.
- Wikipedia retrieval.
- Custom knowledge bases.
- Multi-character conversations.

## Proposed Repository Structure

```text
ai-madridista/
│
├── README.md
├── ARCHITECTURE.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── config/
│   ├── settings.yaml
│   └── characters/
│       └── madridista.json
│
├── src/
│   └── ai_madridista/
│       ├── main.py
│       │
│       ├── core/
│       ├── providers/
│       │   ├── llm/
│       │   ├── stt/
│       │   └── tts/
│       │
│       ├── characters/
│       ├── memory/
│       ├── audio/
│       ├── tools/
│       └── config/
│
├── tests/
│
└── data/
    └── .gitkeep
```

The `data/` directory will hold local application data and databases, which should be excluded from version control.

Secrets, API credentials, recordings, and private conversations must never be committed to GitHub.

The structure is provisional and should evolve as implementation requirements become clearer.

## 6. Development Roadmap

### Phase 1 — Local Model Foundation

**Goal:** Establish a working local AI conversation.

- Install and configure Ollama.
- Download and benchmark Gemma 4.
- Verify GPU acceleration.
- Create the Python project structure.
- Implement the initial LLM provider abstraction.
- Test basic text conversations.

**Milestone:** Communicate with Gemma 4 through Python.

### Phase 2 — AI Madridista Personality

**Goal:** Create the first functional character.

- Define the Madridista personality.
- Implement character configuration loading.
- Establish behavioral instructions.
- Test consistency across multiple conversations.
- Refine comedic behavior and argumentative style.

**Milestone:** A working AI Madridista that can argue through text.

### Phase 3 — Desktop Interface (tabled)

**Goal:** Replace terminal interaction with a native application.

- Build the PySide6 interface.
- Add conversation display.
- Add text input.
- Implement streaming responses.
- Add character selection infrastructure.

**Milestone:** Functional Windows desktop text-chat application.

### Phase 4 — Voice Interaction

**Goal:** Enable natural spoken arguments.

- Implement push-to-talk.
- Integrate faster-whisper.
- Integrate Piper TTS.
- Add audio playback and interruption.
- Optimize latency.

**Milestone:** Speak to AI Madridista and hear it respond.

### Phase 5 — Persistent Memory

**Goal:** Maintain conversations across sessions.

- Implement SQLite storage.
- Save conversation history.
- Restore previous sessions.
- Introduce character-specific memory.
- Add memory deletion controls.

**Milestone:** AI Madridista can remember previous arguments.

### Phase 6 — External Tools

**Goal:** Give the character access to current information.

- Implement the tool interface.
- Add optional web search.
- Introduce source attribution.
- Test tool execution with local models.
- Add permission controls.

**Milestone:** AI Madridista can argue about current football events using retrieved information.

### Phase 7 — Cloud Provider Support

**Goal:** Enable optional paid models without restructuring the application.

- Implement cloud LLM adapters.
- Add cloud STT/TTS alternatives.
- Configure API credentials securely.
- Add usage and cost tracking.
- Test local/cloud provider switching.
- Add budget safeguards.

**Milestone:** Switch between local and cloud services through configuration.

### Phase 8 — Expansion and Experimentation

Potential future features:

- Multiple AI personalities.
- AI-to-AI arguments.
- Animated avatars.
- Emotional voice delivery.
- Football-specific knowledge retrieval.
- More advanced long-term memory.
- Character-specific tools.
- Additional local model support.

These are possibilities, not initial requirements.

## 7. Engineering Principles

**Local-first:** Core functionality should work without paid APIs.

**Provider independence:** Models, speech services, and search providers must remain interchangeable.

**Configuration over code changes:** Routine changes to models and character settings should not require editing application logic.

**Incremental development:** Each phase should produce a testable result before the next begins.

**Performance awareness:** Prioritize responsive conversations and efficient GPU usage.

**Cost awareness:** Cloud features remain optional, with usage tracking and spending safeguards.

**Testability:** Core logic should be testable without the desktop interface or active model services.

**Extensibility:** New characters, tools, and providers should be easy to add.

## 8. Current Decisions and Open Questions

### Confirmed

- Python.
- Ollama as the initial runtime.
- Gemma 4 as the first model candidate.
- RTX 3070 with 8 GB VRAM.
- 32 GB system RAM.
- Push-to-talk and text interaction.
- Persistent memory.
- Multiple-character architecture.
- Local-first operation.
- Optional cloud integration.
- GitHub-hosted development.

### To Be Determined

- Exact Gemma 4 quantization.
- Actual local inference performance.
- Push-to-talk keyboard shortcut.
- Piper voice selection.
- Speech streaming strategy.
- Memory retrieval and summarization policies.
- Web search provider.
- Character personality details.
- Desktop visual design.
- Packaging and distribution strategy.

## 9. Definition of Success

The first complete version should allow me to open the terminal and launch AI Madridista, and argue with it using either text or push-to-talk voice.

The character should respond with a consistent comedic personality, speak its responses, remember previous conversations, and optionally retrieve current football information.

All core functionality should operate locally without requiring paid cloud services.

Cloud models and additional characters should be possible without redesigning the application.

---

**Document status:** Living architecture document. Decisions, technologies, and milestones may be revised throughout development.
