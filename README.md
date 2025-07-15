# Simple Dictation App for macOS

A minimal dictation app that uses OpenAI's Whisper API for speech-to-text conversion with global hotkey support and auto-pasting.

## Features

- **Global Hotkey**: Press Right Command key to start/stop recording
- **OpenAI Integration**: Uses Whisper API for accurate transcription
- **Auto-pasting**: Automatically pastes transcribed text
- **Status Indicator**: System tray icon shows current status
- **Auto-startup**: Optional startup on login
- **macOS Optimized**: Designed specifically for macOS

## Quick Start

1. **Install dependencies**:
   ```bash
   python3 install.py
   ```

2. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Run the app**:
   ```bash
   python3 main.py
   ```

4. **Grant permissions** when prompted:
   - Microphone access
   - Accessibility access (for global hotkeys)

## Usage

1. **Start Recording**: Press and hold Right Command key
2. **Stop Recording**: Release Right Command key
3. **Auto-paste**: Transcribed text is automatically pasted

## Status Icons

- 🎤 Ready
- 🔴 Recording  
- ⏳ Transcribing
- ❌ Error

## Configuration

Configuration is stored in `~/.dictation_config.json`:

```json
{
  "openai_api_key": "your-key",
  "model": "whisper-1",
  "language": "en",
  "hotkey": "cmd_r",
  "auto_paste": true,
  "sample_rate": 16000
}
```

## Auto-startup

To enable auto-startup on login:
```bash
python3 setup_autostart.py
```

To disable:
```bash
python3 setup_autostart.py remove
```

## Requirements

- macOS 10.14+
- Python 3.8+
- OpenAI API key
- Microphone access
- Accessibility permissions

## Troubleshooting

**Permission denied errors:**
- Go to System Preferences > Security & Privacy
- Grant Microphone and Accessibility permissions

**API key errors:**
- Verify your OpenAI API key is valid
- Check the configuration file

**Audio issues:**
- Check microphone permissions
- Verify default audio input device