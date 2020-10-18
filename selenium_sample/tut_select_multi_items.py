import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


url = "https://demos.devexpress.com/aspxeditorsdemos/ListEditors/MultiSelect.aspx"
chrome_path = '/home/xuananh/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                options=chrome_option)
driver.maximize_window()
driver.get(url)

# set select mode to Multiple
driver.find_element_by_id("ControlOptionsTopHolder_lbSelectionMode_B-1").click()
time.sleep(0.5)
driver.find_element_by_id("ControlOptionsTopHolder_lbSelectionMode_DDD_L_LBI1T0").click()
time.sleep(1.5)

# perform Multiple Select
select = driver.find_element_by_id("ContentHolder_lbFeatures_LBT")
options = select.find_elements_by_tag_name("td")

action = ActionChains(driver)

# multi_action = action \
#     .key_down(Keys.CONTROL) \
#     .click(options[0]) \
#     .click(options[3]) \
#     .click(options[5])
# multi_action.perform()

# or
action.key_down(Keys.CONTROL)
action.click(options[0])
action.click(options[3])
action.click(options[5])
action.perform()

print("Multi Select: ")
print(options[0].text)
print(options[3].text)
print(options[5].text)
