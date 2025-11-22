import os
import sys
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-7s [%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

# Import ChromeConnector from the connect_already_open_chrome module
current_dir = os.path.dirname(os.path.abspath(__file__))
connect_chrome_dir = os.path.join(current_dir, '../connect_already_open_chrome')
connect_chrome_file = os.path.join(connect_chrome_dir, 'connect_already_open_chrome.py')

# Check if the file exists
if not os.path.exists(connect_chrome_file):
    logging.error(f"ChromeConnector file not found at {connect_chrome_file}")
    sys.exit(1)

sys.path.insert(0, connect_chrome_dir)

try:
    from connect_already_open_chrome import ChromeConnector
except ImportError as e:
    logging.error(f"Error importing ChromeConnector: {e}")
    logging.error("Make sure connect_already_open_chrome.py is in the connect_already_open_chrome directory.")
    sys.exit(1)


def click_to_submit_button():
    """Click the submit button with the specified HTML structure."""
    connector = ChromeConnector(user_data_dir="/home/xuananh/.config/google-chrome-auto-upload-file-gemini")
    
    try:
        # Get connection to Chrome
        driver = connector.get_or_create_connection()
        
        if not driver:
            logging.error("Could not connect to Chrome")
            return
        
        logging.info("Successfully connected! Looking for submit button...")
        
        # Try multiple strategies to find and click the submit button
        button_found = False
        
        # Strategy 1: Find by class containing 'send-button' and 'submit'
        try:
            logging.info("Trying to find button by class containing 'send-button submit'...")
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.send-button.submit"))
            )
            button.click()
            logging.info("Successfully clicked submit button using class selector!")
            button_found = True
        except TimeoutException:
            logging.warning("Button not found with class selector, trying next method...")
        
        # Strategy 2: Find by aria-label
        if not button_found:
            try:
                logging.info("Trying to find button by aria-label 'Send message'...")
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Send message']"))
                )
                button.click()
                logging.info("Successfully clicked submit button using aria-label!")
                button_found = True
            except TimeoutException:
                logging.warning("Button not found with aria-label, trying next method...")
        
        # Strategy 3: Find by mat-icon with fonticon="send"
        if not button_found:
            try:
                logging.info("Trying to find button by mat-icon with fonticon='send'...")
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button mat-icon[fonticon='send']"))
                )
                # Click the parent button element
                button.find_element(By.XPATH, "./..").click()
                logging.info("Successfully clicked submit button using mat-icon selector!")
                button_found = True
            except TimeoutException:
                logging.warning("Button not found with mat-icon selector, trying next method...")
        
        # Strategy 4: Find by multiple class names
        if not button_found:
            try:
                logging.info("Trying to find button by multiple class names...")
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mdc-icon-button.mat-mdc-icon-button.send-button"))
                )
                button.click()
                logging.info("Successfully clicked submit button using multiple class names!")
                button_found = True
            except TimeoutException:
                logging.warning("Button not found with multiple class names, trying final method...")
        
        # Strategy 5: Find by jslog attribute (last resort)
        if not button_found:
            try:
                logging.info("Trying to find button by jslog attribute...")
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jslog*='173899']"))
                )
                button.click()
                logging.info("Successfully clicked submit button using jslog attribute!")
                button_found = True
            except TimeoutException:
                logging.warning("Button not found with jslog attribute...")
        
        if not button_found:
            logging.error("Could not find the submit button with any of the attempted methods.")
            logging.info("Available buttons on the page:")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for i, btn in enumerate(buttons[:5]):  # Show first 5 buttons
                try:
                    classes = btn.get_attribute("class") or "No classes"
                    aria_label = btn.get_attribute("aria-label") or "No aria-label"
                    logging.debug(f"  Button {i+1}: classes='{classes}', aria-label='{aria_label}'")
                except Exception as e:
                    logging.debug(f"  Button {i+1}: Error getting attributes - {e}")
        else:
            logging.info("Submit button clicked successfully!")
            time.sleep(1)  # Wait a moment to see the result
        
    except Exception as e:
        logging.error(f"Error: {e}")
    
    finally:
        # Note: We're not closing the driver to keep the browser open
        # Uncomment the next line if you want to close the browser
        # connector.close()
        pass


if __name__ == "__main__":
    click_to_submit_button()