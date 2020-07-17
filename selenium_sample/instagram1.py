import json
import time
import traceback
from selenium import webdriver

url = "http://127.0.0.1:59883"
session_id = "c1be6885c037549157e422361c3c1b62"

driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.session_id = session_id


checks_items = ["linh", "lin", "lynh"]
accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")

results = []
count = 0
for account in accounts:
    count += 1
    print(count)
    try:
        acnt = account.find_element_by_xpath(".//div/div/div/div/a").text
    except:
        acnt = ""

    try:
        name = account.find_element_by_xpath(".//div/div/div[2]").text
    except:
        name = ""

    for item in checks_items:
        if item in acnt.lower() or item in name.lower():
            results.append(acnt)

final_result = list(set(results))
print(final_result)

for i in range(0, len(final_result)):
    url = "https://www.instagram.com/" + final_result[i]
    control_string = "window.open('{0}')".format(url)
    driver.execute_script(control_string)
    if i%10 == 0:
        input("Press enter to continue...")





        


