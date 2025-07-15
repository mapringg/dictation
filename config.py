import os
import json
from pathlib import Path
from typing import Optional

class Config:
    def __init__(self):
        self.config_file = Path.home() / ".dictation_config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or use defaults"""
        defaults = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "model": "whisper-1",
            "language": "en",
            "hotkey": "cmd_r",  # Right Command for macOS
            "auto_paste": True,
            "audio_device": None,  # Use default
            "sample_rate": 16000
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    defaults.update(config)
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
        
        # Set attributes
        for key, value in defaults.items():
            setattr(self, key, value)
    
    def save_config(self):
        """Save current configuration to file"""
        config = {
            "openai_api_key": self.openai_api_key,
            "model": self.model,
            "language": self.language,
            "hotkey": self.hotkey,
            "auto_paste": self.auto_paste,
            "audio_device": self.audio_device,
            "sample_rate": self.sample_rate
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def set_api_key(self, api_key: str):
        """Set OpenAI API key"""
        self.openai_api_key = api_key
        self.save_config()
    
    def is_configured(self) -> bool:
        """Check if minimum configuration is present"""
        return bool(self.openai_api_key)