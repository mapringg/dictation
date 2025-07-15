#!/usr/bin/env python3

import os
import sys
from pathlib import Path

def create_launch_agent():
    """Create a LaunchAgent plist file for auto-startup on macOS"""
    
    # Get current script directory
    script_dir = Path(__file__).parent.absolute()
    main_py = script_dir / "main.py"
    
    # LaunchAgents directory
    launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
    launch_agents_dir.mkdir(exist_ok=True)
    
    # Virtual environment Python path
    venv_python = script_dir / "venv" / "bin" / "python"
    
    # Plist content
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.dictation</string>
    <key>ProgramArguments</key>
    <array>
        <string>{venv_python}</string>
        <string>{main_py}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/dictation.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/dictation.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OPENAI_API_KEY</key>
        <string>{os.getenv('OPENAI_API_KEY', '')}</string>
    </dict>
</dict>
</plist>"""
    
    # Write plist file
    plist_path = launch_agents_dir / "com.user.dictation.plist"
    with open(plist_path, 'w') as f:
        f.write(plist_content)
    
    print(f"Created LaunchAgent: {plist_path}")
    
    # Load the launch agent
    os.system(f"launchctl load {plist_path}")
    print("LaunchAgent loaded successfully")
    
    return plist_path

def remove_launch_agent():
    """Remove the LaunchAgent for auto-startup"""
    plist_path = Path.home() / "Library" / "LaunchAgents" / "com.user.dictation.plist"
    
    if plist_path.exists():
        # Unload first
        os.system(f"launchctl unload {plist_path}")
        # Remove file
        plist_path.unlink()
        print("LaunchAgent removed successfully")
    else:
        print("LaunchAgent not found")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_launch_agent()
    else:
        create_launch_agent()