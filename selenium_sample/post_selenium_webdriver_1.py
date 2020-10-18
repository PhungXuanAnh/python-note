from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# set chrome driver and its options
chrome_option = ChromeOptions()
driver = Chrome(executable_path='webdriver/chromedriver',
                options=chrome_option)

# get website
driver.get("http://www.calculator.net/")

# mazimize the browser
driver.maximize_window()

# click on Math Calculators
driver.find_element_by_xpath(".//td[3]/div[2]/a").click()

# click on the percentage calculator
driver.find_element_by_xpath(".//a[@href='/percent-calculator.html' and contains(text(),'Percentage Calculator')]").click()

# enter value 10 in the first number of the percentage calculator
driver.find_element_by_id('cpar1').send_keys('123')

# enter value 50 in the second number of the percentage calculator
driver.find_element_by_id('cpar2').send_keys('555')

# click the calculate button
driver.find_element_by_css_selector('input[value="Calculate"').click()

# get the result based on its xpath
result = driver.find_element_by_xpath(".//p[@class='verybigtext']").text

# print it out to stdout
print(result)
print(driver.find_element_by_xpath(".//p[@class='aaa']"))

# close browser
driver.close()
