"""
Selenium Checkbox Interaction Tutorial - Undetected ChromeDriver Version

This script demonstrates how to interact with checkboxes on a web page using undetected_chromedriver.
The script has been updated to:
1. Use undetected_chromedriver to avoid bot detection
2. Use absolute paths for chromedriver location
3. Use modern Selenium 4+ syntax (By.ID instead of find_element_by_id)
4. Include proper wait conditions and error handling
5. Handle hidden elements using JavaScript clicks
6. Fast startup optimizations

Requirements: pip install undetected-chromedriver
"""

import time
import os
import tempfile
import signal
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

url = "https://www.calculator.net/mortgage-calculator.html"

class TimeoutException(Exception):
    pass

def create_undetected_driver():
    """Create undetected_chromedriver with optimizations and local ChromeDriver"""
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(script_dir, 'webdriver', 'chromedriver')
    
    # Create temporary user data directory
    user_data_dir = tempfile.mkdtemp(prefix="checkbox_test_")
    
    # Setup Chrome options
    opts = uc.ChromeOptions()
    opts.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Fast startup flags
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
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding',
        '--disable-features=VizDisplayCompositor',
        '--disable-ipc-flooding-protection'
    ]
    
    for flag in fast_flags:
        opts.add_argument(flag)
    
    try:
        print("Creating undetected Chrome driver...")
        
        # Setup timeout protection
        def alarm_handler(signum, frame):
            raise TimeoutException("Driver initialization timeout!")
        
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(10)  # 10 second timeout
        
        # Try with local ChromeDriver first
        if os.path.exists(chromedriver_path):
            driver = uc.Chrome(
                options=opts,
                driver_executable_path=chromedriver_path,
                use_subprocess=False,
                version_main=None  # Skip version detection
            )
        else:
            print("Local chromedriver not found, using system version...")
            driver = uc.Chrome(
                options=opts,
                use_subprocess=False,
                version_main=None
            )
        
        signal.alarm(0)  # Cancel alarm
        return driver, user_data_dir
        
    except Exception as e:
        signal.alarm(0)  # Cancel alarm
        print(f"Failed to create undetected Chrome driver: {e}")
        raise

def main():
    print("Starting Checkbox Interaction Tutorial with undetected_chromedriver...")
    start_time = time.time()
    
    driver = None
    user_data_dir = None
    
    try:
        # Create the undetected driver
        driver, user_data_dir = create_undetected_driver()
        driver.maximize_window()
        
        init_time = time.time()
        print(f"Driver initialized in: {init_time - start_time:.3f}s")
        
        # Navigate to the test page
        print(f"Loading page: {url}")
        driver.get(url)
        
        # Wait for page to load and element to be present
        wait = WebDriverWait(driver, 10)
        
        # First, let's wait for the page to load completely
        time.sleep(2)
        
        # Find the checkbox element
        print("Looking for checkbox element...")
        checkbox_element = driver.find_element(By.ID, 'caddoptional')
        
        # Scroll to the element to make sure it's visible
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_element)
        time.sleep(1)
        
        print(f"Element found - Is Displayed: {checkbox_element.is_displayed()}, Is Enabled: {checkbox_element.is_enabled()}")
        
        # Check if element is initially selected
        initial_state = checkbox_element.is_selected()
        print(f'Initial state - Is Selected: {initial_state}')
        
        # Try to click using JavaScript (more reliable for hidden elements)
        print("Clicking checkbox using JavaScript...")
        driver.execute_script("arguments[0].click();", checkbox_element)
        print('✓ Checkbox clicked successfully using JavaScript!')
        
        # Wait a moment for the state to change
        time.sleep(0.5)
        
        # Check the state after clicking
        final_state = checkbox_element.is_selected()
        print(f'Final state - Is Selected: {final_state}')
        print('Is Enabled:   ', checkbox_element.is_enabled())
        print('Is Displayed: ', checkbox_element.is_displayed())
        
        # Verify the click worked
        if initial_state != final_state:
            print('✓ Checkbox state changed successfully!')
            print('✓ Test PASSED - Checkbox interaction worked with undetected_chromedriver!')
        else:
            print('⚠ Checkbox state did not change - might need different approach')
        
        # Demonstrate toggling the checkbox again
        print("\nToggling checkbox again to demonstrate...")
        driver.execute_script("arguments[0].click();", checkbox_element)
        time.sleep(0.5)
        
        toggle_state = checkbox_element.is_selected()
        print(f'After toggle - Is Selected: {toggle_state}')
        
        if toggle_state == initial_state:
            print('✓ Checkbox successfully toggled back to initial state!')
        
        # Give some time to see the result
        print("\nTest completed. Browser will close in 3 seconds...")
        time.sleep(3)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Let's check if the element exists...")
        
        if driver:
            try:
                # Let's check what elements are available
                elements = driver.find_elements(By.TAG_NAME, "input")
                print(f"Found {len(elements)} input elements")
                
                for i, element in enumerate(elements[:10]):  # Check first 10 elements
                    try:
                        element_id = element.get_attribute('id')
                        element_type = element.get_attribute('type')
                        element_name = element.get_attribute('name')
                        if element_id or element_type in ['checkbox', 'radio']:
                            print(f"Element {i}: id='{element_id}', type='{element_type}', name='{element_name}'")
                    except:
                        pass
            except Exception as debug_error:
                print(f"Debug error: {debug_error}")
        else:
            print("Driver not initialized, cannot debug elements")

    finally:
        # Clean up
        if driver:
            try:
                driver.quit()
                print("Driver closed successfully")
            except:
                print("Error closing driver")
        
        # Clean up temporary directory
        if user_data_dir and os.path.exists(user_data_dir):
            try:
                import shutil
                shutil.rmtree(user_data_dir, ignore_errors=True)
                print("Temporary files cleaned up")
            except:
                pass
        
        total_time = time.time() - start_time
        print(f"Total execution time: {total_time:.3f}s")

if __name__ == "__main__":
    main()