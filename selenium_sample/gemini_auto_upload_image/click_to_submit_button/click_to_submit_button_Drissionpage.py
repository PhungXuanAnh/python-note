import time
import os
import subprocess
import sys
import socket
import signal
import logging
from DrissionPage import ChromiumPage

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


def click_to_submit_button():
    """Click the submit button with multiple fallback strategies using DrissionPage."""
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
        logging.info("Looking for submit button...")
        
        # Try multiple strategies to find and click the submit button
        button_found = False
        
        # Strategy 1: Find by class containing 'send-button' and 'submit'
        try:
            logging.info("Trying to find button by class containing 'send-button submit'...")
            button = page.ele("css:button.send-button.submit", timeout=10)
            if button:
                button.click()
                logging.info("Successfully clicked submit button using class selector!")
                button_found = True
        except Exception as e:
            logging.warning(f"Button not found with class selector: {e}, trying next method...")
        
        # Strategy 2: Find by aria-label
        if not button_found:
            try:
                logging.info("Trying to find button by aria-label 'Send message'...")
                button = page.ele("css:button[aria-label='Send message']", timeout=5)
                if button:
                    button.click()
                    logging.info("Successfully clicked submit button using aria-label!")
                    button_found = True
            except Exception as e:
                logging.warning(f"Button not found with aria-label: {e}, trying next method...")
        
        # Strategy 3: Find by mat-icon with fonticon="send"
        if not button_found:
            try:
                logging.info("Trying to find button by mat-icon with fonticon='send'...")
                icon = page.ele("css:button mat-icon[fonticon='send']", timeout=5)
                if icon:
                    # Get parent button element
                    button = icon.parent()
                    button.click()
                    logging.info("Successfully clicked submit button using mat-icon selector!")
                    button_found = True
            except Exception as e:
                logging.warning(f"Button not found with mat-icon selector: {e}, trying next method...")
        
        # Strategy 4: Find by multiple class names
        if not button_found:
            try:
                logging.info("Trying to find button by multiple class names...")
                button = page.ele("css:button.mdc-icon-button.mat-mdc-icon-button.send-button", timeout=5)
                if button:
                    button.click()
                    logging.info("Successfully clicked submit button using multiple class names!")
                    button_found = True
            except Exception as e:
                logging.warning(f"Button not found with multiple class names: {e}, trying final method...")
        
        # Strategy 5: Find by jslog attribute (last resort)
        if not button_found:
            try:
                logging.info("Trying to find button by jslog attribute...")
                button = page.ele("css:button[jslog*='173899']", timeout=5)
                if button:
                    button.click()
                    logging.info("Successfully clicked submit button using jslog attribute!")
                    button_found = True
            except Exception as e:
                logging.warning(f"Button not found with jslog attribute: {e}")
        
        if not button_found:
            logging.error("Could not find the submit button with any of the attempted methods.")
            logging.info("Available buttons on the page:")
            buttons = page.eles("tag:button")
            for i, btn in enumerate(buttons[:5]):  # Show first 5 buttons
                try:
                    classes = btn.attr("class") or "No classes"
                    aria_label = btn.attr("aria-label") or "No aria-label"
                    logging.debug(f"  Button {i+1}: classes='{classes}', aria-label='{aria_label}'")
                except Exception as e:
                    logging.debug(f"  Button {i+1}: Error getting attributes - {e}")
        else:
            logging.info("Submit button clicked successfully!")
            time.sleep(1)  # Wait a moment to see the result
        
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
    """Main function for testing - runs the script directly."""
    logging.info("Testing click_to_submit_button...")
    success = click_to_submit_button()
    
    if success:
        logging.info("Script completed successfully!")
    else:
        logging.error("Script completed with errors.")
    logging.info("Script finished.")


if __name__ == "__main__":
    main()
