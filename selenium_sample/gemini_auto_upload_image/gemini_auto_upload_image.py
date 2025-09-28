import time
import os
import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/home/xuananh/Documents/gemini-auto/.chrome-user-data")
options.add_argument('--profile-directory=Default')

# Ultra-fast flags from undetected_chromedriver_sample.py
fast_flags = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-extensions',
    '--disable-default-apps',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-logging',
    '--log-level=3',
    '--silent',
    # '--window-size=200,150',  # Commented out to see the browser
    # '--window-position=-5000,-5000', # Commented out to see the browser
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-features=VizDisplayCompositor',
    '--disable-ipc-flooding-protection'
]
for flag in fast_flags:
    options.add_argument(flag)

# Use local ChromeDriver binary
script_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(script_dir, "webdriver", "chromedriver")

# Initialize WebDriver
driver = uc.Chrome(
    options=options,
    driver_executable_path=chromedriver_path,
    use_subprocess=False,
    version_main=None  # Skip version detection
)

try:
    # Navigate to Gemini
    driver.get("https://gemini.google.com")
    print("Navigated to https://gemini.google.com")

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
            ['bash', script_path], 
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
            subprocess.Popen(['bash', script_path], env=env)
            time.sleep(5)  # Give it time to complete
            print("Fallback method executed.")
        except Exception as e2:
            print(f"Fallback method also failed: {e2}")

    # Keep the browser open for observation
    print("Automation finished. Browser will remain open.")

finally:
    # Close the browser - commented out to keep browser open
    # driver.quit()
    print("Script finished.")
