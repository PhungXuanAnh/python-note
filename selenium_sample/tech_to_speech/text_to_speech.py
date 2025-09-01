import os
import time
import subprocess
import threading
import wave
from typing import Optional, Dict, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            
            print("Recording stopped")
    
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

def smart_text_splitter(text: str, max_length: int = 5000) -> List[str]:
    """
    Split text intelligently to stay under max_length
    1. First try to keep whole text
    2. If too long, split by sentences (.)
    3. If sentences still too long, split by clauses (,)
    4. If still too long, force split at max_length
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    
    # Split by sentences first
    sentences = text.split('.')
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # If adding this sentence would exceed limit
        if len(current_chunk) + len(sentence) + 1 > max_length:
            # Save current chunk if it has content
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            # If this single sentence is still too long, split by commas
            if len(sentence) > max_length:
                comma_parts = sentence.split(',')
                current_comma_chunk = ""
                
                for part in comma_parts:
                    part = part.strip()
                    if not part:
                        continue
                    
                    # If adding this part would exceed limit
                    if len(current_comma_chunk) + len(part) + 1 > max_length:
                        # Save current comma chunk if it has content
                        if current_comma_chunk:
                            chunks.append(current_comma_chunk.strip())
                            current_comma_chunk = ""
                        
                        # If this single part is STILL too long, force split
                        if len(part) > max_length:
                            # Force split at max_length boundaries
                            for j in range(0, len(part), max_length):
                                chunks.append(part[j:j+max_length])
                        else:
                            current_comma_chunk = part
                    else:
                        # Add to current comma chunk
                        if current_comma_chunk:
                            current_comma_chunk += ", " + part
                        else:
                            current_comma_chunk = part
                
                # Add remaining comma chunk
                if current_comma_chunk:
                    chunks.append(current_comma_chunk.strip())
            else:
                # Sentence is fine, start new chunk with it
                current_chunk = sentence
        else:
            # Add to current chunk
            if current_chunk:
                current_chunk += ". " + sentence
            else:
                current_chunk = sentence
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def read_entire_file(file_path: str) -> str:
    """
    Read the entire file content as a single string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def wait_for_speech_completion(driver, wait_timeout: int = 60):
    """
    Wait for Google Translate to complete reading the text by monitoring button state changes
    
    Args:
        driver: Selenium WebDriver instance
        wait_timeout: Maximum time to wait in seconds
    
    Returns:
        bool: True if speech completed successfully, False if timed out
    """
    start_time = time.time()
    
    # Define button selectors
    listen_button_selectors = [
        "button[aria-label='Listen to source text']",
        "button[aria-label*='Listen']",
        ".VfPpkd-Bz112c[aria-label*='Listen']",
        "button[data-tooltip='Listen']"
    ]
    
    stop_button_selectors = [
        "button[aria-label='Stop listening to source text']",
        "button[aria-label*='Stop listening']",
        "button[aria-label*='Stop']",
        ".VfPpkd-Bz112c[aria-label*='Stop']",
        "button[data-tooltip='Stop']"
    ]
    
    print("Waiting for speech to start...")
    
    # First, wait for the Stop button to appear (speech started)
    stop_button_appeared = False
    for _ in range(10):  # Wait up to 5 seconds for speech to start
        for selector in stop_button_selectors:
            try:
                stop_button = driver.find_element(By.CSS_SELECTOR, selector)
                if stop_button.is_displayed():
                    print("Speech started (Stop button detected)")
                    stop_button_appeared = True
                    break
            except:
                continue
        
        if stop_button_appeared:
            break
        
        time.sleep(0.5)
    
    if not stop_button_appeared:
        print("Warning: Stop button not detected, speech may not have started properly")
        return False
    
    print("Waiting for speech to complete...")
    
    # Now wait for the Listen button to reappear (speech finished)
    while time.time() - start_time < wait_timeout:
        try:
            # Check if any Stop button is still present and visible
            stop_button_still_present = False
            for selector in stop_button_selectors:
                try:
                    stop_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if stop_button.is_displayed():
                        stop_button_still_present = True
                        break
                except:
                    continue
            
            # If no Stop button is present, speech should be finished
            if not stop_button_still_present:
                # Double-check by looking for Listen button
                for selector in listen_button_selectors:
                    try:
                        listen_button = driver.find_element(By.CSS_SELECTOR, selector)
                        if listen_button.is_displayed() and listen_button.is_enabled():
                            print("Speech completed (Listen button reappeared)")
                            return True
                    except:
                        continue
            
            time.sleep(0.5)  # Check every 500ms
            
        except Exception as e:
            print(f"Error during speech completion detection: {e}")
            break
    
    print("Speech completion detection timed out")
    return False

def main():
    """Main function for Google Translate recording"""
    # Initialize the audio recorder
    recorder = PulseAudioRecorder()
    audio_source = "V_MIC_remapped_from_OUT_speaker"
    output_dir = os.path.dirname(os.path.realpath(__file__))

    try:
        # 1. Open selenium with Google Translate URL
        driver = webdriver.Chrome()
        driver.get("https://translate.google.com/?sl=vi&tl=en&op=translate")

        # 2. Wait for the page to load completely
        wait = WebDriverWait(driver, 15)
        
        # Wait for Google Translate to fully load
        print("Waiting for Google Translate to load...")
        time.sleep(5)  # Give extra time for the page to fully load

        # 3. Find the text area for input
        text_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Source text']")))
        
        # Read the entire file content
        input_file = "input.txt"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        input_file = os.path.join(dir_path, input_file)

        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found!")
            print("Please create an input.txt file with your Vietnamese text.")
            return
        
        print(f"Reading content from {input_file}...")
        full_text = read_entire_file(input_file)
        
        if not full_text:
            print("No content found in input.txt file!")
            return
        
        print(f"Full text length: {len(full_text)} characters")
        
        # Split text into chunks for processing
        text_chunks = smart_text_splitter(full_text, 5000)
        print(f"Split into {len(text_chunks)} chunks for processing")
        
        # Start recording for the ENTIRE session (all chunks)
        print("Starting audio recording for entire input.txt...")
        recorder.start_recording(audio_source)
        time.sleep(0.5)  # Small delay to ensure recording started
        
        chunk_count = 0
        
        for chunk in text_chunks:
            chunk_count += 1
            
            print(f"\nProcessing chunk {chunk_count}/{len(text_chunks)}")
            print(f"Chunk length: {len(chunk)} characters")
            print(f"Chunk preview: {chunk[:100]}...")  # Show first 100 chars for debugging
            
            # Clear and input the chunk using JavaScript for better reliability
            try:
                # Method 1: Try using JavaScript to set the value directly
                driver.execute_script("arguments[0].value = '';", text_area)
                driver.execute_script("arguments[0].value = arguments[1];", text_area, chunk)
                
                # Trigger input event to make Google Translate recognize the text
                driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", text_area)
                
            except Exception as e:
                print(f"JavaScript method failed: {e}, trying Selenium method...")
                # Fallback to original method
                text_area.clear()
                text_area.send_keys(chunk)
            
            # Wait for the text to be processed
            print("Waiting for text to be processed...")
            time.sleep(3)  # Wait for Google Translate to process the text
            
            # Verify text was actually populated correctly
            actual_text = driver.execute_script("return arguments[0].value;", text_area)
            if not actual_text or len(actual_text.strip()) < len(chunk.strip()) * 0.8:  # Allow 20% tolerance
                print(f"Text population failed. Expected ~{len(chunk)} chars, got {len(actual_text) if actual_text else 0} chars")
                print("Skipping this chunk...")
                continue
            
            print(f"Text populated successfully: {len(actual_text)} characters")

            # Find and click the Listen button
            listen_button_selectors = [
                "button[aria-label='Listen to source text']",
                "button[aria-label*='Listen']",
                ".VfPpkd-Bz112c[aria-label*='Listen']",
                "button[data-tooltip='Listen']"
            ]
            
            listen_button = None
            for selector in listen_button_selectors:
                try:
                    listen_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    print(f"Found Listen button with selector: {selector}")
                    break
                except:
                    continue
            
            if not listen_button:
                print("Listen button not found after text input, skipping this chunk...")
                continue

            # Click the Listen button
            print("Clicking Listen button...")
            listen_button.click()
            
            # Wait for speech to complete using improved detection
            speech_completed = wait_for_speech_completion(driver, wait_timeout=600)
            
            if not speech_completed:
                print("Warning: Speech completion detection failed, continuing anyway...")
            
            # Brief pause before next chunk to ensure clean transition
            print("Moving to the next chunk...")
            time.sleep(2)

        # Stop recording after ALL chunks are processed
        print(f"\nCompleted processing all {len(text_chunks)} chunks")
        print("Stopping audio recording...")
        recorder.stop_recording()

        # Save the single audio file containing the entire input.txt
        audio_filename = "complete_input_audio.wav"
        audio_path = os.path.join(output_dir, audio_filename)
        
        if recorder.save_recording(audio_path):
            print(f"Complete audio saved: {audio_path}")
        else:
            print("Failed to save complete audio file")

        print(f"Audio file saved in: {output_dir}")
        print("\nBrowser will remain open for inspection. Close manually when done.")
        
        # Keep the browser open
        input("Press Enter to close the browser...")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        print("Browser will remain open for inspection. Close manually when done.")
        input("Press Enter to close the browser...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Browser will remain open for inspection. Close manually when done.")
        input("Press Enter to close the browser...")
    finally:
        # Clean up
        recorder.cleanup()
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()