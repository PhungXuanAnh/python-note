import traceback
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


def click_button_translate_by_voice(driver):
    buttons = driver.find_elements(By.XPATH, '//button[@aria-label="Translate by voice"]')
    
    if len(buttons) == 2:
        try:
            buttons[0].click()
        except ElementNotInteractableException:
            buttons[1].click()
        except NoSuchElementException:
            print("no button Translate by voice")
        except:
            traceback.print_exc()
    elif len(buttons) == 1:
        print("google translate is listening...")
    else:
        return "button element has changed, please update xpath"
