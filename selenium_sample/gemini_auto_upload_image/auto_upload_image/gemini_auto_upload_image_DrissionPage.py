import time
import os
import subprocess
import sys
import socket
import signal
import logging
from DrissionPage import ChromiumPage, ChromiumOptions

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-7s [%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def cleanup_chrome(process):
    if process:
        try:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/PID', str(process.pid), '/T'], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.kill(process.pid, signal.SIGTERM)
        except Exception:
            pass

def gemini_auto_upload(file_path):
    """Main function to perform Gemini auto upload using DrissionPage.
    
    Args:
        file_path (str): Full path to the file to upload
    
    Returns:
        ChromiumPage: The page object if successful, None otherwise
    """
    # Configuration
    user_data_dir = os.path.expanduser("/home/xuananh/.config/google-chrome-auto-upload-file-gemini")
    browser_path = "/usr/bin/google-chrome"  # Default for Linux
    
    chrome_process = None
    chrome_already_running = False
    
    try:
        # Check if Chrome is already running on port 9222
        if is_port_in_use(9222):
            logging.info("Chrome is already running on port 9222. Connecting to existing instance...")
            chrome_already_running = True
        else:
            # Launch Chrome manually
            chrome_cmd = [
                browser_path,
                f"--user-data-dir={user_data_dir}",
                "--profile-directory=Default",
                "--remote-debugging-port=9222",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-first-run",
                "--no-default-browser-check",
                # Fast flags
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--disable-default-apps",
                "--disable-logging",
                "--log-level=3",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-features=VizDisplayCompositor",
                "--disable-ipc-flooding-protection"
            ]

            logging.info("Launching new Chrome instance...")
            chrome_process = subprocess.Popen(
                chrome_cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from parent process
            )

            # Wait for Chrome to be ready
            logging.info("Waiting for Chrome to be ready...")
            for _ in range(10):
                if is_port_in_use(9222):
                    logging.info("Chrome is ready on port 9222")
                    break
                time.sleep(1)
            else:
                logging.error("Chrome failed to start on port 9222")
                cleanup_chrome(chrome_process)
                return None

            time.sleep(2)

        # Connect DrissionPage to existing instance
        logging.info("Connecting to Chrome...")
        page = ChromiumPage(addr_or_opts='127.0.0.1:9222')
        
        if not page:
            logging.error("Could not connect to Chrome. Exiting.")
            return None
        
        logging.info("Successfully connected to Chrome!")
        
        # Check current URL and navigate only if needed
        current_url = page.url
        logging.info(f"Current URL: {current_url}")
        
        if "gemini.google.com" in current_url:
            logging.info("Already on Gemini domain, skipping navigation.")
        else:
            logging.info("Navigating to https://gemini.google.com")
            page.get("https://gemini.google.com")
            logging.info("Navigated to Gemini")

        # 1. Click the 'Open upload file menu' button
        logging.info("Looking for the 'Open upload file menu' button...")
        upload_menu_button = page.ele("css:button[aria-label='Open upload file menu']", timeout=20)
        upload_menu_button.click()
        logging.info("Clicked the 'Open upload file menu' button.")
        
        time.sleep(0.5)

        # 2. Click the 'Upload files' button to open the dialog
        logging.info("Looking for the 'Upload files' button...")
        upload_files_button = page.ele("xpath://button[.//div[text()='Upload files']]", timeout=20)
        upload_files_button.click()
        logging.info("Clicked the 'Upload files' button.")

        # 3. Call the shell script to handle file dialog
        logging.info("Calling auto_file_picker.sh to handle file dialog...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "auto_file_picker.sh")
        
        env = os.environ.copy()
        env['DISPLAY'] = env.get('DISPLAY', ':0')
        
        try:
            # Use Popen with real-time output like run_command in subprocess_sample.py
            command = f"bash {script_path} {file_path}"
            logging.debug(f"Running command: {command}")
            
            p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env
            )
            
            # Read output in real-time
            output = ""
            while True:
                out = p.stdout.readline()
                if out == b'' and p.poll() is not None:
                    break
                if out != b'':
                    line = out.strip().decode()
                    logging.debug(line)
                    output += out.decode()
            
            return_code = p.poll()
            if return_code == 0:
                logging.info("File picker script executed successfully.")
            else:
                logging.error(f"File picker script failed with return code: {return_code}")
                
        except Exception as e:
            logging.error(f"Error running file picker script: {e}")

        logging.info("Automation finished successfully!")
        logging.info("Browser will remain open for your use.")
        return page
        
    except Exception as e:
        logging.error(f"Error during automation: {e}")
        return None
    
    finally:
        # Note: We're not closing the page to keep the browser open
        logging.info("Chrome browser remains open.")
        pass


def main():
    """Main function for testing - runs the script directly with a default file path."""
    # Default file path - can be changed as needed
    default_file_path = "/home/xuananh/Downloads/vm-screenshot/image.png"
    
    logging.info(f"Testing gemini_auto_upload with file: {default_file_path}")
    success = gemini_auto_upload(default_file_path)
    
    if success:
        logging.info("Script completed successfully!")
    else:
        logging.error("Script completed with errors.")
    logging.info("Script finished.")

if __name__ == "__main__":
    main()
