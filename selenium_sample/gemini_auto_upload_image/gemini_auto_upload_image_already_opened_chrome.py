#!/usr/bin/env python3
"""
Gemini auto upload image script using already opened Chrome browser.
Uses ChromeConnector to connect to existing Chrome instances.
"""

import time
import os
import subprocess
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import ChromeConnector from the connect_already_open_chrome module
current_dir = os.path.dirname(os.path.abspath(__file__))
connect_chrome_dir = os.path.join(current_dir, '../connect_already_open_chrome')
connect_chrome_file = os.path.join(connect_chrome_dir, 'connect_already_open_chrome.py')

# Check if the file exists
if not os.path.exists(connect_chrome_file):
    print(f"Error: ChromeConnector file not found at {connect_chrome_file}")
    sys.exit(1)

sys.path.insert(0, connect_chrome_dir)

try:
    from connect_already_open_chrome import ChromeConnector
except ImportError as e:
    print(f"Error importing ChromeConnector: {e}")
    print("Make sure connect_already_open_chrome.py is in the connect_already_open_chrome directory.")
    sys.exit(1)


def gemini_auto_upload(file_path):
    """Main function to perform Gemini auto upload using existing Chrome.
    
    Args:
        file_path (str): Full path to the file to upload
    """
    # Initialize ChromeConnector
    connector = ChromeConnector(user_data_dir="/home/xuananh/.config/google-chrome-auto-upload-file-gemini")
    
    try:
        # Get connection to Chrome
        driver = connector.get_or_create_connection()
        
        if not driver:
            print("Could not connect to Chrome. Exiting.")
            return False
        
        print("Successfully connected to Chrome!")
        
        # Check if current tab is already on Gemini domain
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        if "gemini.google.com" not in current_url:
            # Navigate to Gemini
            driver.get("https://gemini.google.com")
            print("Navigated to https://gemini.google.com")
        else:
            print("Already on Gemini domain, skipping navigation.")

        # 1. Click the 'Open upload file menu' button
        print("Looking for the 'Open upload file menu' button...")
        upload_menu_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Open upload file menu']"))
        )
        upload_menu_button.click()
        print("Clicked the 'Open upload file menu' button.")

        # 2. Click the 'Upload files' button to open the dialog
        print("Looking for the 'Upload files' button...")
        upload_files_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Upload files']]"))
        )
        upload_files_button.click()
        print("Clicked the 'Upload files' button.")

        # 3. Call the shell script to handle file dialog
        print("Calling gemini_auto_file_picker.sh to handle file dialog...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "gemini_auto_file_picker.sh")
        
        # Prepare environment variables for GUI operations
        env = os.environ.copy()
        env['DISPLAY'] = env.get('DISPLAY', ':0')
        
        try:
            # Method 1: Try with proper environment and shell=True
            result = subprocess.run(
                ['bash', script_path, file_path], 
                capture_output=True, 
                text=True, 
                timeout=30,
                env=env,
                shell=False
            )
            if result.returncode == 0:
                print("File picker script executed successfully.")
                print(result.stdout)
            else:
                print(f"File picker script failed with return code: {result.returncode}")
                print(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("File picker script timed out.")
        except Exception as e:
            print(f"Error running file picker script: {e}")
            
            # Method 2: Fallback - try running without capturing output
            print("Trying fallback method without capturing output...")
            try:
                subprocess.Popen(['bash', script_path, file_path], env=env)
                time.sleep(5)  # Give it time to complete
                print("Fallback method executed.")
            except Exception as e2:
                print(f"Fallback method also failed: {e2}")

        # Keep the browser open for a while to observe
        print("Automation finished. Browser will remain open.")
        return driver
        
    except Exception as e:
        print(f"Error during automation: {e}")
        return None
    
    finally:
        # Clean up using the connector
        print("Cleaning up...")
        # Note: We're not closing the driver to keep the browser open
        # Uncomment the next line if you want to close the browser
        # connector.close()
        pass


if __name__ == "__main__":
    # Default file path - can be changed as needed
    default_file_path = "/home/xuananh/Downloads/vm-screenshot/image.png"
    success = gemini_auto_upload(default_file_path)
    if success:
        print("Script completed successfully!")
    else:
        print("Script completed with errors.")
    print("Script finished.")
