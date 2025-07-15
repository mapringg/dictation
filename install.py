#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python 3.8+ is available"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_config():
    """Setup initial configuration"""
    from config import Config
    
    config = Config()
    
    if not config.openai_api_key:
        print("\n⚠️  OpenAI API key not found!")
        print("Please set your OpenAI API key:")
        print("1. Export it as environment variable: export OPENAI_API_KEY='your-key-here'")
        print("2. Or add it to your shell profile (~/.zshrc or ~/.bash_profile)")
        print("3. Or create ~/.dictation_config.json with your API key")
        
        api_key = input("\nEnter your OpenAI API key (or press Enter to skip): ").strip()
        if api_key:
            config.set_api_key(api_key)
            print("✓ API key saved to configuration")
    else:
        print("✓ OpenAI API key configured")

def check_permissions():
    """Check macOS permissions"""
    print("\n📋 macOS Permissions Required:")
    print("1. Microphone Access - Required for audio recording")
    print("2. Accessibility Access - Required for global hotkeys and auto-pasting")
    print("3. You may be prompted for these permissions when first running the app")
    print("4. If permissions are denied, go to System Preferences > Security & Privacy")

def install_autostart():
    """Ask user if they want to install auto-startup"""
    response = input("\nDo you want to enable auto-startup on login? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        try:
            subprocess.check_call([sys.executable, "setup_autostart.py"])
            print("✓ Auto-startup configured")
        except subprocess.CalledProcessError as e:
            print(f"Error setting up auto-startup: {e}")

def main():
    print("🎤 Dictation App Installation")
    print("=" * 30)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup configuration
    setup_config()
    
    # Check permissions
    check_permissions()
    
    # Ask about auto-startup
    install_autostart()
    
    print("\n✅ Installation complete!")
    print("\nTo run the app:")
    print("  python3 main.py")
    print("\nTo test the app:")
    print("  1. Press and hold Right Command key to start recording")
    print("  2. Speak something")
    print("  3. Release Right Command key to stop and transcribe")
    print("  4. Text will be automatically pasted")

if __name__ == "__main__":
    main()