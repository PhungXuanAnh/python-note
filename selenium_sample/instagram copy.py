import json
import time
import traceback
from selenium import webdriver

url = "http://127.0.0.1:53915"
session_id = "3f30b75b963cfa1396c7b8f5da10860a"

driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.session_id = session_id

# move mouse to follower and scroll
accounts = None
while not accounts:
    try:
        accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")
        time.sleep(1)
    except Exception as e:
        print(e.args)

# print(accounts[0].text)
# print(accounts[0].find_element_by_xpath(".//div/div/div/div/a").text)
# print(accounts[0].find_element_by_xpath(".//div/div/div/div[2]").text)

for account in accounts:
    # print(account.find_element_by_xpath(".//div/div/div/div/a").text)
    try:
        print(account.find_element_by_xpath(".//div/div/div/div[2]").text)
    except:
        pass
    # if "linh" in account.text:
    #     print(account.text)

exit(0)
last_accounts = accounts[-1]
driver.execute_script("arguments[0].scrollIntoView(true);", last_accounts)
print(driver.command_executor._url)
print(driver.session_id)


while True:
    try:
        new_accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")
        driver.execute_script("arguments[0].scrollIntoView(true);", last_accounts)
        time.sleep(1)
        last_accounts = new_accounts[-1]
        print(len(new_accounts))
        if len(new_accounts) > 3600:
            break
    except Exception as e:
        print(e.args)
        time.sleep(1)
        new_accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")
        last_accounts = new_accounts[-1]
        
print(driver.command_executor._url)
print(driver.session_id)





        


