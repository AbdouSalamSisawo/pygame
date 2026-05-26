# Adaptive AI-Driven Educational Game for Early Childhood Literacy

## Course Information
- **Institution:** School of Computing and Informatics, Albukhary International University
- **Course Code:** CCC1243 Artificial Intelligence
- **Project Type:** Group Project

## Course Learning Outcome (CLO)
Develop intelligent systems to solve computational problems (P5, PLO6).

## Project Overview
Early childhood learners (ages 4–6) have unique cognitive, physical, and literacy needs. Static software often fails to adapt to repeated mistakes, short attention spans, and emerging language skills. This project delivers a **child-friendly, adaptive educational game** built in Python to help young learners develop literacy skills. The game demonstrates **AI-driven adaptation** by tracking behavior, adjusting difficulty, and providing contextual hints and encouragement.

## Educational Focus
This implementation focuses on **Vocabulary Learning**:
- Recognize words
- Associate words with images
- Understand pronunciation (via optional TTS)
- Build memory and literacy familiarity

## Key Features
- **Bright, clean, visual UI** with large buttons and minimal text
- **Instruction screen** for self-guided learning
- **Two activity types**: image-to-word and word-to-image matching
- **Adaptive AI** that tracks mistakes and adapts difficulty and hints
- **Non-punitive scoring** with progress stars
- **Audio feedback** for correct/incorrect responses
- **Progress persistence** (settings and learning stats)
- **Optional Voice User Interface (VUI)** using offline STT/TTS

## System Requirements
- **Python:** 3.10+ recommended (3.12 tested)
- **OS:** Windows 10/11 recommended
- **Audio:** Speakers and microphone (for VUI)
- **Dependencies:** listed in `requirements.txt`

## Installation
```bash
pip install -r requirements.txt
```

## Run the Game
```bash
python main.py
```

## Controls
- **Mouse:** Click/tap to select answers and buttons
- **Keyboard:**
  - Left / Right arrows: move selection
  - Enter / Space: confirm selection
  - Esc: return to main menu

## Gameplay Flow
1. **Main Menu**: Start Game, Instructions, Settings, Exit
2. **Instructions**: Simple, kid-friendly how-to-play
3. **Game**:
   - Match pictures to words or words to pictures
   - Receive immediate feedback
   - Earn stars for progress
4. **Session Complete**:
   - Play again or return home

## Adaptive Intelligence (AI)
The game tracks performance per word and adapts dynamically:
- Reduces options after repeated mistakes
- Highlights correct answers as hints
- Reinforces difficult words more often
- Provides positive, encouraging feedback

## Voice User Interface (Optional)
This project includes **offline voice input/output**:
- **Speech-to-Text (STT):** Vosk (offline, local model download)
- **Text-to-Speech (TTS):** pyttsx3

### Voice Input
- Tap **Mic** during gameplay
- Speak a visible word (e.g., "sun", "book", "hat")
- The game selects and grades the matching option
- Voice commands:
  - "menu", "home", "exit": return to main menu
  - "repeat": repeat the current prompt

### Voice Output
The game can speak:
- Instructions
- Prompts and hints
- Correct/incorrect feedback
- Encouragement at session end

### Voice Settings
In **Settings**, you can:
- Enable/disable voice input
- Enable/disable voice output
- Adjust voice volume

> Note: The Vosk speech model downloads automatically on first use and is cached locally in `data/`.
> Online STT is **not** integrated yet; it requires an API key and a provider integration.

## Project Structure
```
d:\pygame
├── main.py                 # App entry point
├── config.py               # Global settings and colors
├── scene.py                # Scene manager
├── ui.py                   # UI helpers and components
├── assets.py               # Placeholder icon rendering
├── audio.py                # Sound effects
├── voice.py                # VUI (offline STT/TTS)
├── data/
│   └── vocab.json          # Demo vocabulary dataset
├── gameplay/
│   └── rounds.py           # Round generation logic
├── ai/
│   └── adaptive.py         # Adaptive tracker
├── screens/
│   ├── menu.py
│   ├── instructions.py
│   ├── settings.py
│   └── game.py
└── storage/
    └── progress.py         # Save/load progress
```

## UI/UX Design
- Minimal text, high visual clarity
- Large interactive elements
- Consistent spacing and clean panels
- Friendly, encouraging messaging

## Scoring
The scoring system is **non-punitive**:
- Correct answers increase score
- Stars represent progress
- Incorrect answers trigger hints, not penalties

## Demo Vocabulary
The demo dataset is intentionally small and child-friendly:
- **Nature:** sun, moon, leaf, tree
- **Toys:** ball, kite
- **Animals:** fish, bird
- **Food/School/Transport/Clothes:** apple, book, car, hat

## Settings & Persistence
- **Settings** are stored in `data/progress.json`
- Includes sound volume, difficulty bias, voice input/output toggles, and voice volume
- Progress stats track correct/incorrect answers and recent sessions

## Error Handling & Fallbacks
- Voice input is optional and gracefully disabled if dependencies or microphone are unavailable
- If speech is not detected within the timeout, the game shows a friendly message and continues
- All core gameplay remains fully functional without voice features

## Testing Checklist (Manual)
1. Launch app and navigate all menu items.
2. Complete a game session and return home.
3. Verify hints and adaptive behavior after repeated mistakes.
4. Toggle voice input/output and confirm feedback.
5. Confirm progress is saved after exit and restored on restart.

## YouTube Video Presentation Guidelines
1. **Length:** 5–10 minutes.
2. **Upload:** Public or Unlisted; paste active link in eLearning submission.
3. **All members must present:** each person speaks and explains their contribution.
4. **Content must include:**
   - Introduction of group members and objectives
   - Technical architecture walkthrough
   - Live runtime demo showing instructions, scoring, and AI adaptation

## Acknowledgements
This project was built for CCC1243 Artificial Intelligence and aligns with the course learning outcomes and project requirements.
