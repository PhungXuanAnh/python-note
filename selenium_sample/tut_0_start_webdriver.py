from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service


# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code
# chrome_options.add_argument('--profile-directory=Profile 16')
# chrome_options.add_argument("user-data-dir=/home/xuananh/.config/google-chrome1") #Path to your chrome profile

service = Service(executable_path='webdriver/chromedriver')
driver = Chrome(service=service,options=chrome_options)
driver.maximize_window()
driver.get("https://translate.google.com/?sl=vi&tl=en&op=translate")
