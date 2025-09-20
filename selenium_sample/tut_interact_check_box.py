"""
Selenium Checkbox Interaction Tutorial

This script demonstrates how to interact with checkboxes on a web page.
The script has been updated to:
1. Use absolute paths for chromedriver location
2. Use modern Selenium 4+ syntax (By.ID instead of find_element_by_id)
3. Include proper wait conditions and error handling
4. Handle hidden elements using JavaScript clicks

Alternative modern approach (requires: pip install webdriver-manager):
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    # This automatically downloads and manages the correct chromedriver version
"""

import time
import os
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

url = "https://www.calculator.net/mortgage-calculator.html"

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(script_dir, 'webdriver', 'chromedriver')

# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
# Optional: add headless mode for running without GUI
# chrome_option.add_argument('--headless')

service = Service(executable_path=chromedriver_path)
driver = Chrome(service=service, options=chrome_option)
driver.maximize_window()
driver.get(url)

# Wait for page to load and element to be clickable
wait = WebDriverWait(driver, 10)

try:
    # First, let's wait for the page to load completely
    time.sleep(2)
    
    # Find the checkbox element
    checkbox_element = driver.find_element(By.ID, 'caddoptional')
    
    # Scroll to the element to make sure it's visible
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_element)
    time.sleep(1)
    
    print(f"Element found - Is Displayed: {checkbox_element.is_displayed()}, Is Enabled: {checkbox_element.is_enabled()}")
    
    # Check if element is initially selected
    initial_state = checkbox_element.is_selected()
    print(f'Initial state - Is Selected: {initial_state}')
    
    # Try to click using JavaScript (more reliable for hidden elements)
    driver.execute_script("arguments[0].click();", checkbox_element)
    print('✓ Checkbox clicked successfully using JavaScript!')
    
    # Check the state after clicking
    final_state = checkbox_element.is_selected()
    print(f'Final state - Is Selected: {final_state}')
    print('Is Enabled:   ', checkbox_element.is_enabled())
    print('Is Displayed: ', checkbox_element.is_displayed())
    
    # Verify the click worked
    if initial_state != final_state:
        print('✓ Checkbox state changed successfully!')
    else:
        print('⚠ Checkbox state did not change - might need different approach')
    
    # Give some time to see the result
    time.sleep(3)
    
except Exception as e:
    print(f"Error: {e}")
    print("Let's check if the element exists...")
    
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

finally:
    # Close the browser
    driver.quit()


