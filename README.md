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
1) KeyError in choice evaluation

Observed failure (example):
```text
self.evaluate_choice(option["item"])
                         ~~~~~~^^^^^^^^
KeyError: 'item'
```
What this means: some entries in the option layout are missing the expected `item` key when the game calls `evaluate_choice()`.
Suggested steps to investigate and fix:
- Reproduce the failure and add logging around `compute_option_layout()` and where `option_layout` is used to confirm each element's keys.
- Check `gameplay/rounds.py` and `screens/game.py::compute_option_layout()` to ensure `item` is always added and not removed by later processing.
- Guard `evaluate_choice()` with a safe lookup (e.g., `option.get('item')`) and log a detailed error rather than crashing.
- Add unit tests that build round states with corner cases (zero options, eliminated indices) to prevent regressions.

2) Voice assistant unreliable / not working

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

These images are intended for documentation only. If you publish this repository, avoid committing personal or large binary files beyond these illustrative screenshots.

## Polished Overview (quick)
Word Explorer is a compact, pedagogical game built with Python and Pygame to practice early vocabulary. It ships with a curated demo word set and simple adaptive logic that increases exposure to words the learner struggles with.

- Platform: Python 3.10+ (Windows tested)
- UI: Pygame, keyboard + mouse controls; optional offline voice input/output
- Persistence: Local JSON save at `data/progress.json` (do not commit)

### Professional notes for contributors
- Keep the `data/vocab.json` dataset curated and small for quick sessions.
- Treat `data/progress.json` and any downloaded `vosk-model-*` directories as local-only artifacts; they are in `.gitignore` and should not be committed.
- When adding screenshots, keep them in `screenshots/` and follow the existing naming convention `NN-description.png` so the README references remain accurate.
