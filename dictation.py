import asyncio
import logging
import threading
import time
import os
import subprocess
from threading import Event
from typing import Optional

import numpy as np
import sounddevice as sd
import openai
from pynput import keyboard

from config import Config


logger = logging.getLogger(__name__)

class AudioRecorder:
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
        self.dtype = np.float32
        self.recording = False
        self.audio_data = []
        self.stream = None
        
    def start_recording(self):
        if self.recording:
            return
            
        self.recording = True
        self.audio_data = []
        
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio callback status: {status}")
            if self.recording:
                self.audio_data.append(indata.copy())
        
        try:
            self.stream = sd.InputStream(
                callback=audio_callback,
                channels=self.channels,
                samplerate=self.sample_rate,
                dtype=self.dtype
            )
            self.stream.start()
            logger.info("Recording started")
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.recording = False
    
    def stop_recording(self) -> Optional[np.ndarray]:
        if not self.recording:
            return None
            
        self.recording = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        if self.audio_data:
            audio = np.concatenate(self.audio_data, axis=0)
            logger.info(f"Recording stopped, captured {len(audio)} samples")
            return audio
        
        return None

class GroqTranscriber:
    def __init__(self, config: Config):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
    
    async def transcribe(self, audio_data: np.ndarray) -> str:
        try:
            # Convert to int16 for saving as FLAC (as recommended by Groq)
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Save to temporary file as FLAC for better compression
            import tempfile
            import subprocess
            
            # First save as WAV, then convert to FLAC using ffmpeg
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav_temp:
                with tempfile.NamedTemporaryFile(suffix='.flac', delete=False) as flac_temp:
                    # Save as WAV first
                    import wave
                    with wave.open(wav_temp.name, 'wb') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)
                        wav_file.setframerate(16000)
                        wav_file.writeframes(audio_int16.tobytes())
                    
                    # Convert to FLAC using ffmpeg (if available), otherwise use WAV
                    try:
                        subprocess.run([
                            'ffmpeg', '-i', wav_temp.name, '-c:a', 'flac', 
                            '-ar', '16000', '-ac', '1', '-y', flac_temp.name
                        ], check=True, capture_output=True)
                        audio_file_path = flac_temp.name
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        # Fallback to WAV if ffmpeg not available
                        logger.warning("ffmpeg not available, using WAV format")
                        audio_file_path = wav_temp.name
                    
                    # Transcribe with Groq
                    with open(audio_file_path, 'rb') as audio_file:
                        response = await asyncio.to_thread(
                            self.client.audio.transcriptions.create,
                            model=self.config.model,
                            file=audio_file,
                            language=self.config.language,
                            temperature=0  # Set to 0 for consistent results as recommended
                        )
                    
                    # Clean up temp files
                    os.unlink(wav_temp.name)
                    if audio_file_path == flac_temp.name:
                        os.unlink(flac_temp.name)
                    
                    return response.text.strip()
                
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return ""

class ClipboardPaster:
    @staticmethod
    def paste_text(text: str):
        try:
            # Copy to clipboard
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            
            # Simulate Cmd+V
            time.sleep(0.1)
            from pynput.keyboard import Key, Controller
            kb = Controller()
            kb.press(Key.cmd)
            kb.press('v')
            kb.release('v')
            kb.release(Key.cmd)
            
            logger.info(f"Pasted text: {text[:50]}...")
        except Exception as e:
            logger.error(f"Failed to paste text: {e}")

class StatusIndicator:
    def __init__(self, dictation_app):
        self.dictation_app = dictation_app
        self.status_item = None
        self._setup_status_bar()
    
    def _setup_status_bar(self):
        try:
            import Cocoa
            from Foundation import NSObject
            
            # Initialize NSApplication if not already done
            app = Cocoa.NSApplication.sharedApplication()
            app.setActivationPolicy_(Cocoa.NSApplicationActivationPolicyAccessory)
            
            # Create status bar item
            status_bar = Cocoa.NSStatusBar.systemStatusBar()
            self.status_item = status_bar.statusItemWithLength_(Cocoa.NSVariableStatusItemLength)
            
            # Set initial title
            self.status_item.setTitle_("🎤")
            self.status_item.setHighlightMode_(True)
            
            logger.info("Status bar initialized")
        except ImportError:
            logger.warning("PyObjC not available, status bar disabled")
            self.status_item = None
        except Exception as e:
            logger.error(f"Failed to setup status bar: {e}")
            self.status_item = None
    
    def set_status(self, status: str):
        status_icons = {
            "ready": "🎤",
            "recording": "🔴",
            "transcribing": "⚡",
            "error": "❌"
        }
        
        status_messages = {
            "ready": "Ready for dictation",
            "recording": "Recording...",
            "transcribing": "Transcribing audio...",
            "error": "Error occurred"
        }
        
        icon = status_icons.get(status, "🎤")
        message = status_messages.get(status, status)
        
        if self.status_item:
            self.status_item.setTitle_(icon)
            self.status_item.setToolTip_(message)
        
        logger.info(f"Status: {message}")
    
    def run(self):
        try:
            import Cocoa
            # Run the app event loop
            Cocoa.NSApp.run()
        except ImportError:
            # Fallback if PyObjC not available
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

class DictationApp:
    def __init__(self):
        self.config = Config()
        
        if not self.config.is_configured():
            raise ValueError("Groq API key not configured. Set GROQ_API_KEY environment variable or run setup.")
        
        self.recorder = AudioRecorder()
        self.transcriber = GroqTranscriber(self.config)
        self.paster = ClipboardPaster()
        self.status_indicator = StatusIndicator(self)
        
        self.is_recording = False
        self.shutdown_event = Event()
        
        # Double-press detection for stop recording
        self.last_cmd_r_time = 0
        self.double_press_threshold = 0.5  # 500ms window for double press
        
        # Set up keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
    
    def on_key_press(self, key):
        try:
            # Right Command key for macOS
            if key == keyboard.Key.cmd_r:
                current_time = time.time()
                time_since_last_press = current_time - self.last_cmd_r_time
                
                if not self.is_recording:
                    # Check for double press to start recording
                    if time_since_last_press <= self.double_press_threshold and self.last_cmd_r_time > 0:
                        # Double press detected - start recording
                        self.start_recording()
                    else:
                        # Single press - just update timestamp for potential double press
                        self.last_cmd_r_time = current_time
                else:
                    # Check for double press to stop recording
                    if time_since_last_press <= self.double_press_threshold:
                        # Double press detected - stop recording
                        self.stop_recording()
                    else:
                        # Single press while recording - update timestamp for potential double press
                        self.last_cmd_r_time = current_time
            # Escape key to cancel recording
            elif key == keyboard.Key.esc and self.is_recording:
                self.cancel_recording()
        except AttributeError:
            pass
    
    def start_recording(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        self.status_indicator.set_status("recording")
        self.recorder.start_recording()
        logger.info("Started recording")
    
    def stop_recording(self):
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.status_indicator.set_status("transcribing")
        
        audio_data = self.recorder.stop_recording()
        if audio_data is not None and len(audio_data) > 0:
            # Process transcription in background
            threading.Thread(target=self._process_transcription, args=(audio_data,)).start()
        else:
            self.status_indicator.set_status("ready")
    
    def cancel_recording(self):
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.status_indicator.set_status("ready")
        
        # Stop recording without processing audio
        self.recorder.stop_recording()
        logger.info("Recording cancelled")
    
    def _process_transcription(self, audio_data):
        try:
            # Run async transcription in thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            text = loop.run_until_complete(self.transcriber.transcribe(audio_data))
            loop.close()
            
            if text:
                self.paster.paste_text(text)
                logger.info(f"Transcribed and pasted: {text}")
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            self.status_indicator.set_status("error")
            time.sleep(2)  # Show error for 2 seconds
        finally:
            self.status_indicator.set_status("ready")
    
    def run(self):
        self.status_indicator.set_status("ready")
        self.listener.start()
        
        try:
            self.status_indicator.run()
        finally:
            self.listener.stop()
            self.shutdown_event.set()