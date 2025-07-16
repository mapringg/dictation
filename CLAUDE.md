# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a macOS dictation app that provides global hotkey-based speech-to-text transcription using Groq's API. The app runs as a background process with system tray integration and automatic text pasting.

## Development Commands

### Setup and Installation
```bash
# Install dependencies and setup
python3 install.py

# Set up auto-startup on login
python3 setup_autostart.py

# Remove auto-startup
python3 setup_autostart.py remove
```

### Running the Application
```bash
# Run the main application
python3 main.py

# Run with virtual environment (if available)
./venv/bin/python main.py
```

## Project Architecture

### Core Components

- **main.py**: Entry point with logging setup and signal handling
- **dictation.py**: Main application logic containing all core classes:
  - `DictationApp`: Main orchestrator handling global hotkeys and workflow
  - `AudioRecorder`: Handles audio recording using sounddevice
  - `GroqTranscriber`: Manages Groq API calls for transcription
  - `ClipboardPaster`: Handles automatic text pasting via clipboard and Cmd+V
  - `StatusIndicator`: System tray icon showing app status using PyObjC/Cocoa
- **config.py**: Configuration management with JSON file storage at `~/.dictation_config.json`

### Key Features

- **Global Hotkeys**: Double-press Right Command key for record/stop (500ms window), Escape for cancel
- **Status Icons**: 🎤 (ready), 🔴 (recording), ⚡ (transcribing), ❌ (error)
- **Groq Integration**: Uses `whisper-large-v3-turbo` model
- **Auto-pasting**: Automatic text insertion via clipboard + Cmd+V simulation
- **macOS Integration**: LaunchAgent support for auto-startup

### Dependencies

Key Python packages:
- `openai>=1.0.0` - OpenAI-compatible client for Groq API
- `sounddevice>=0.4.0` - Audio recording
- `numpy>=1.20.0` - Audio data processing
- `pynput>=1.7.0` - Global hotkey handling
- `pyobjc-framework-Cocoa>=9.0` - macOS system tray integration

Optional system dependencies:
- `ffmpeg` - For optimal audio compression (FLAC format), falls back to WAV if unavailable

### Configuration

Configuration is stored in `~/.dictation_config.json` with these key settings:
- `groq_api_key`: Groq API key
- `model`: Transcription model (default: "whisper-large-v3-turbo")
- `language`: Language code (default: "en")
- `hotkey`: Hotkey setting (default: "cmd_r")
- `auto_paste`: Auto-pasting enabled (default: true)
- `sample_rate`: Audio sample rate (default: 16000)

### Logging

Logs are written to both stdout and `/tmp/dictation.log` for debugging.

## Testing

This project does not currently have unit tests. When adding tests, consider testing:
- Audio recording functionality
- Groq API integration
- Configuration loading/saving
- Hotkey detection
- Status indicator updates