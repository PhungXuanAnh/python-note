#!/usr/bin/env python3
"""
PulseAudio Sound Recorder
Records audio directly from PulseAudio sources using parec
"""

import subprocess
import threading
import time
import wave
import sys
from typing import Optional, Dict, List

class PulseAudioRecorder:
    def __init__(self, 
                 sample_rate: int = 44100,
                 channels: int = 2,
                 chunk_size: int = 1024):
        """
        Initialize the PulseAudio recorder
        
        Args:
            sample_rate: Sample rate in Hz (default: 44100)
            channels: Number of audio channels (default: 2 for stereo)
            chunk_size: Buffer size for reading (default: 1024)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.recording = False
        self.frames = []
        self.process = None
        
    def get_pulseaudio_sources(self) -> Dict[str, str]:
        """Get PulseAudio source information"""
        sources = {}
        try:
            # Get PulseAudio sources
            result = subprocess.run(['pactl', 'list', 'sources'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return sources
                
            current_source = None
            current_name = None
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                # Look for source entries
                if line.startswith('Source #'):
                    current_source = line
                elif line.startswith('Name: ') and current_source:
                    current_name = line.split('Name: ', 1)[1]
                elif line.startswith('Description: ') and current_name:
                    description = line.split('Description: ', 1)[1]
                    sources[current_name] = description
                    current_source = None
                    current_name = None
                    
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Error: pactl command not found. Make sure PulseAudio is installed.")
            
        return sources
    
    def list_sources(self):
        """List all available PulseAudio sources"""
        sources = self.get_pulseaudio_sources()
        
        if not sources:
            print("No PulseAudio sources found or pactl not available")
            return []
            
        print("Available PulseAudio Sources:")
        print("-" * 70)
        
        source_list = list(sources.items())
        for i, (name, description) in enumerate(source_list):
            print(f"{i}: {description}")
            print(f"   Internal name: {name}")
            print()
            
        return source_list
    
    def select_source(self) -> Optional[str]:
        """Interactive selection of PulseAudio source"""
        source_list = self.list_sources()
        
        if not source_list:
            return None
        
        try:
            choice = input("Select PulseAudio source (enter number): ").strip()
            index = int(choice)
            if 0 <= index < len(source_list):
                return source_list[index][0]  # Return internal name
            else:
                print("Invalid selection")
                return None
        except (ValueError, KeyboardInterrupt):
            return None
    
    def start_recording(self, source_name: str):
        """
        Start recording from a PulseAudio source
        
        Args:
            source_name: PulseAudio source name
        """
        try:
            # Build parec command
            cmd = [
                'parec',
                '--device', source_name,
                f'--format=s16le',
                f'--rate={self.sample_rate}',
                f'--channels={self.channels}'
            ]
            
            print(f"Recording from: {source_name}")
            print("Press Ctrl+C to stop recording")
            
            # Start parec process
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.recording = True
            self.frames = []
            
            # Start recording thread
            self._record_thread = threading.Thread(target=self._record_loop)
            self._record_thread.start()
            
            print("Recording started!")
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.recording = False
    
    def _record_loop(self):
        """Internal recording loop"""
        try:
            while self.recording and self.process:
                # Read data in chunks (2 bytes per sample for s16le)
                chunk_bytes = self.chunk_size * 2 * self.channels
                data = self.process.stdout.read(chunk_bytes)
                if not data:
                    break
                self.frames.append(data)
        except Exception as e:
            print(f"Recording error: {e}")
        finally:
            self.recording = False
    
    def stop_recording(self):
        """Stop the current recording"""
        if self.recording:
            self.recording = False
            
            # Wait for recording thread to finish
            if hasattr(self, '_record_thread'):
                self._record_thread.join()
            
            # Terminate parec process
            if self.process:
                self.process.terminate()
                self.process.wait()
                self.process = None
            
            print("\nRecording stopped")
    
    def record_for_duration(self, source_name: str, duration: float):
        """
        Record from a PulseAudio source for a specific duration
        
        Args:
            source_name: PulseAudio source name
            duration: Recording duration in seconds
        """
        self.start_recording(source_name)
        time.sleep(duration)
        self.stop_recording()
    
    def save_recording(self, filename: str):
        """
        Save the recorded audio to a WAV file
        
        Args:
            filename: Output filename (should end with .wav)
        """
        if not self.frames:
            print("No audio data to save")
            return False
        
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 2 bytes for s16le format
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
            
            # Calculate duration
            total_bytes = sum(len(frame) for frame in self.frames)
            duration = total_bytes / (self.sample_rate * self.channels * 2)
            print(f"Audio saved to '{filename}' ({duration:.2f} seconds)")
            return True
            
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_recording()

def main():
    """Main function for PulseAudio recording"""
    recorder = PulseAudioRecorder()
    
    try:
        # Select PulseAudio source
        source_name = recorder.select_source()
        if not source_name:
            print("No source selected, exiting.")
            return
        
        # Get recording duration
        try:
            duration_str = input("Enter recording duration in seconds (or press Enter for manual stop): ").strip()
            duration = float(duration_str) if duration_str else None
        except ValueError:
            duration = None
        
        # Start recording
        try:
            if duration:
                print(f"\nRecording for {duration} seconds...")
                recorder.record_for_duration(source_name, duration)
            else:
                recorder.start_recording(source_name)
                try:
                    while recorder.recording:
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    print("\nStopping recording...")
                finally:
                    recorder.stop_recording()
        except KeyboardInterrupt:
            print("\nStopping recording...")
            recorder.stop_recording()
        
        # Always try to save the recording if we have data
        if recorder.frames:
            try:
                output_file = input("Enter output filename (default: recording.wav): ").strip()
                if not output_file:
                    output_file = "recording.wav"
                
                if not output_file.endswith('.wav'):
                    output_file += '.wav'
                
                recorder.save_recording(output_file)
            except KeyboardInterrupt:
                # If user interrupts during filename input, save with default name
                print("\nSaving with default filename...")
                recorder.save_recording("recording.wav")
        else:
            print("No audio data recorded")
        
    except KeyboardInterrupt:
        print("\nRecording interrupted by user")
        # Ensure recording is stopped
        recorder.stop_recording()
        # Try to save any recorded data
        if recorder.frames:
            print("Saving recorded audio...")
            recorder.save_recording("recording.wav")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Try to save any recorded data
        if recorder.frames:
            recorder.save_recording("recording.wav")
    finally:
        recorder.cleanup()

if __name__ == "__main__":
    main()