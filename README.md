# Word Explorer

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/github/license/AbdouSalamSisawo/pygame)](LICENSE)
[![GitHub Workflow Status](https://github.com/AbdouSalamSisawo/pygame/actions/workflows/ci.yml/badge.svg)](https://github.com/AbdouSalamSisawo/pygame/actions)
[![Last commit](https://img.shields.io/github/last-commit/AbdouSalamSisawo/pygame)](https://github.com/AbdouSalamSisawo/pygame/commits)
[![Issues](https://img.shields.io/github/issues/AbdouSalamSisawo/pygame)](https://github.com/AbdouSalamSisawo/pygame/issues)
[![Release](https://img.shields.io/github/v/release/AbdouSalamSisawo/pygame?sort=semver)](https://github.com/AbdouSalamSisawo/pygame/releases)

Word Explorer is a small Python/Pygame literacy game for early learners. It focuses on simple word recognition, picture-word matching, and gentle adaptive feedback so repeated mistakes become more guided instead of more punishing.

## Current Status
The project is playable end to end in its current form.

- Main menu, instructions, settings, and game scenes are implemented.
- The game supports mouse input and keyboard navigation.
- Rounds alternate between picture-to-word and word-to-picture matching.
- The adaptive tracker reduces pressure on difficult words by changing option count and hint behavior.
- Progress is saved locally, including settings, totals, word stats, and recent sessions.
- Optional voice input and voice output are supported when the extra dependencies are installed.

## Features
- Friendly, child-oriented UI with large buttons and simple layouts.
- Vocabulary-based matching gameplay with colored icon cards.
- Non-punitive scoring with stars and positive feedback.
- Difficulty bias settings: easy, normal, and hard.
- Offline voice output with pyttsx3.
- Offline voice input with Vosk and sounddevice.

## Project Layout
```text
d:\pygame
├── main.py
├── config.py
├── scene.py
├── ui.py
├── assets.py
├── audio.py
├── voice.py
├── README.md
├── requirements.txt
├── screenshots/
├── data/
│   ├── vocab.json
│   └── vosk-model-small-en-us-0.15/
├── ai/
│   └── adaptive.py
├── gameplay/
│   └── rounds.py
├── screens/
│   ├── menu.py
│   ├── instructions.py
│   ├── settings.py
│   └── game.py
└── storage/
    └── progress.py
```

## How It Works
`main.py` loads the vocabulary, saved progress, audio, and voice systems, then starts the menu scene.

The gameplay loop in `screens/game.py` runs a 10-round session. Each round is built by `gameplay/rounds.py` and uses `ai/adaptive.py` to choose the target word and control how many options are shown. Correct answers increase the score and stars. Incorrect answers trigger hints and make the next rounds easier for that word.

## Controls
- Mouse: click buttons, cards, and menu items.
- Keyboard: left/right to move between options, Enter or Space to confirm, Esc to return to the menu.
- Voice input: press Mic during gameplay and say a visible word or a command like menu, home, exit, or repeat.

## Settings And Save Data
Settings are managed from the Settings screen and stored locally in `data/progress.json`.

Saved data includes:
- sound volume
- voice input toggle
- voice output toggle
- voice volume
- difficulty bias
- per-word stats
- total correct, wrong, and stars
- recent session summaries

The progress file is generated locally and should not be committed. The Vosk speech model is downloaded on first use and cached in `data/`.

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Requirements
- Python 3.10 or newer is recommended.
- Windows is the primary tested platform.
- Voice features require microphone access and the optional packages in `requirements.txt`.

## Vocabulary Set
The demo vocabulary is intentionally small and child-friendly.

- Nature: sun, moon, leaf, tree
- Toys: ball, kite
- Animals: fish, bird
- Food and school: apple, book
- Transport and clothes: car, hat

## Notes
- If voice input is unavailable, the game still works normally.
- If the speech model is not ready yet, the app shows a status message and continues.
- The app is designed to fail gracefully when optional audio or microphone dependencies are missing.

## Known issues (for contributors)
1) Voice assistant unreliable / not working

Symptoms: voice input may report "Voice input not installed" or fail during recognition; `VoiceManager` may show status messages but not deliver expected text to the game.
Quick checks:
- Confirm optional dependencies are installed (`vosk`, `sounddevice`, `pyttsx3`) and the Vosk model exists in `data/`.
- Check microphone permissions on the host platform and that the sample rate/format expected by `sounddevice` is available.
- Watch the `VoiceInput._set_status()` messages and `voice.status` used in the UI for clues.

Possible improvements / alternatives for contributors:
- Improve Vosk robustness: pre-download the model (the code supports this), validate `MODEL_DIR`, and add clearer error messages when model loading fails.
- Use a different STT backend if Vosk proves unreliable: options include OpenAI Whisper (local or API), Google Cloud Speech-to-Text, or Microsoft Azure Speech. Each has trade-offs (offline vs. cloud, cost, accuracy). For example, `whisper` (local) can run offline and often gives robust transcriptions but requires GPU or more CPU.
- For a cloud-backed approach, wrap calls with retries and graceful fallbacks to keyboard input when network or quota fails.
- Add automated integration tests or a small debug route that records a short audio clip and runs recognition locally to verify the audio pipeline.

Please note: per project request, this README documents the issue but does not attempt an automatic code fix. Contributors should follow the diagnostic steps above and open a PR with tests.

## Acknowledgements
Built for CCC1243 Artificial Intelligence as an adaptive literacy game prototype.

---

## Screenshots
The repository includes example screenshots under the `screenshots/` folder. These images illustrate core parts of the application and are referenced here so readers can quickly understand the UI and flow.

- Main menu: [screenshots/01-home-menu.png](screenshots/01-home-menu.png) — app title, subtitle, and navigation buttons (Start, Instructions, Settings, Exit).
- Instructions: [screenshots/02-instructions.png](screenshots/02-instructions.png) — the how-to-play panel with short, child-friendly directions.
- Game round: [screenshots/03-game-round.png](screenshots/03-game-round.png) — an active round showing the prompt, option cards/buttons, current score and stars.
- Hint state: [screenshots/04-hint-state.png](screenshots/04-hint-state.png) — after a wrong answer, a hint and eliminated options are visible.
- Settings: [screenshots/05-settings.png](screenshots/05-settings.png) — volume, voice toggles, voice volume, difficulty bias, and reset controls.
- Session complete: [screenshots/06-session-complete.png](screenshots/06-session-complete.png) — end-of-session summary with Play Again / Return Home options.

These images are intended for documentation only.

## Polished Overview (quick)
Word Explorer is a compact, pedagogical game built with Python and Pygame to practice early vocabulary. It ships with a curated demo word set and simple adaptive logic that increases exposure to words the learner struggles with.

- Platform: Python 3.10+ (Windows tested)
- UI: Pygame, keyboard + mouse controls; optional offline voice input/output
- Persistence: Local JSON save at `data/progress.json` (do not commit)

### Professional notes for contributors
- Keep the `data/vocab.json` dataset curated and small for quick sessions.
- Treat `data/progress.json` and any downloaded `vosk-model-*` directories as local-only artifacts; they are in `.gitignore` and should not be committed.
- When adding screenshots, keep them in `screenshots/` and follow the existing naming convention `NN-description.png` so the README references remain accurate.

---

## Contributing & Roadmap
This project is a teaching-focused prototype; contributions that improve reliability, testing, and voice interaction are especially welcome. Below are concrete, actionable improvements contributors can take on.

1) Core quality and CI
- Add a lightweight unit test suite for core logic (`ai/adaptive.py`, `gameplay/rounds.py`, and `storage/progress.py`). Use `pytest` and run tests in CI (GitHub Actions).
- Add linting (`ruff`/`flake8`) and type checks (`mypy`) to the CI pipeline.
- Add a simple GitHub Actions workflow that runs lint, tests, and a quick smoke test that imports the game modules.

2) Voice assistant (priority)
The voice assistant is useful but fragile; improving it will greatly increase the project polish. Suggested tasks:
- Improve model handling: ensure the Vosk model is downloaded and validated before enabling voice input. Move download logic to an idempotent helper and expose a `--preload-voice-model` CLI or a Settings button.
- Add robust error handling and user feedback: show explicit UI messages for missing dependencies, audio device errors, or model-corruption.
- Add an integration test that records or replays a short WAV sample and runs through the `VoiceInput` pipeline to verify recognition end-to-end.
- Add a fallback transcription option using other backends (configurable):
    - Local Whisper (via `whisper` or `faster-whisper`) for higher accuracy on short phrases. Note: local Whisper is CPU/GPU intensive.
    - Cloud STT (Google Cloud Speech-to-Text, Azure Speech, or OpenAI Whisper API) for a hosted option; wrap calls with retries and rate-limit handling.
- Improve selection resilience: after recognition, map recognized text to option words using fuzzy matching (e.g., `difflib.SequenceMatcher` or `rapidfuzz`) to tolerate partial matches and small transcription errors.

3) UX and debugging tools
- Add a small debug overlay or log window that shows the latest STT partial/final results and Vosk status for troubleshooting (useful for contributors and QA).
- Add a `--screenshot` or headless mode that can capture interface screenshots for automated visual tests.

4) Packaging and distribution
- Add `setuptools` packaging or a `pyproject.toml` to make the project installable for contributors: `pip install -e .`.
- Pin `setuptools<81` in `requirements.txt` or CI to avoid the `pkg_resources` deprecation warning seen on some machines.

5) Accessibility & localization
- Improve accessibility: keyboard focus indicators, larger target areas, and color-contrast checks.
- Externalize UI strings into a `strings.json` and offer a simple localization loader for other languages.

How to prioritize
- Short-term (1–2 days): add tests for `AdaptiveTracker`, add the Vosk model preloader, and fix the voice crash (already addressed).
- Mid-term (1–2 weeks): CI workflow, fuzzy matching for voice, integration test for voice pipeline.
- Longer-term: alternative STT backends (Whisper or cloud), packaging, and localization.

If you'd like, I can scaffold a minimal GitHub Actions workflow that runs tests and linting and then open a PR with those files.
