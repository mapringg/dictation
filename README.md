# Simple Dictation App for macOS

A minimal dictation app that uses OpenAI's transcription API for speech-to-text conversion with global hotkey support and auto-pasting.

## Features

- **Global Hotkey**: Press Right Command key to start/stop recording
- **Cancel Recording**: Press Escape key to cancel current recording
- **OpenAI Integration**: Uses gpt-4o-mini-transcribe model for accurate transcription
- **Auto-pasting**: Automatically pastes transcribed text to active application
- **Status Indicator**: System tray icon shows current status (🎤/🔴/⚡/❌)
- **Auto-startup**: Optional startup on login
- **macOS Optimized**: Designed specifically for macOS with native integrations

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

1. **Start Recording**: Press Right Command key to start recording
2. **Stop Recording**: Press Right Command key again to stop and transcribe
3. **Cancel Recording**: Press Escape key to cancel without transcribing
4. **Auto-paste**: Transcribed text is automatically pasted to the active application

## Status Icons

- 🎤 Ready for dictation
- 🔴 Recording audio
- ⚡ Transcribing audio
- ❌ Error occurred

## Configuration

Configuration is stored in `~/.dictation_config.json`:

```json
{
  "openai_api_key": "your-key",
  "model": "gpt-4o-mini-transcribe",
  "language": "en",
  "hotkey": "cmd_r",
  "auto_paste": true,
  "audio_device": null,
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