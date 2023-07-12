import time
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

chrome_options = ChromeOptions()
# chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code
# chrome_options.add_argument('--profile-directory=Profile 16')
chrome_options.add_argument("user-data-dir=/home/xuananh/.config/google-chrome1") #Path to your chrome profile
chrome_options.add_argument("class=chrome1")    # NOTE: it must add this argument while running chrome to allow new chrome instance
                                                # be linked to new icon and be grouped in another icon in dock of ubuntu launcher
                                                # for example this is command to run chrome in terminal:
                                                # google-chrome --user-data-dir=/home/xuananh/.config/google-chrome1 --class="chrome1"
                                                # Add StartupWMClass=chrome1 to this file :
                                                # /home/xuananh/Dropbox/Work/Other/conf.d/google-chrome/desktop-shortcut/chrome1.desktop 
                                                # copy or create soft link to ~/.local/share/applications/
                                                # open new chrome shortcut from menu of launcher to see new icon in dock
                                                # then run this python file
                                                # reference: https://askubuntu.com/a/367851/1077704

service = Service(executable_path='webdriver/chromedriver')
driver = Chrome(service=service,options=chrome_options)
driver.get("https://translate.google.com/?sl=en&tl=vi")

# enable translate by voice
try:
    driver.find_element(By.XPATH, '//button[@aria-label="Translate by voice" and @aria-pressed="false"]').click()
except NoSuchElementException:
    print("aaaaaaaaaaaa 1: no button Translate by voice")
except:
    traceback.print_exc()

# reset when characters used is more than 1000
characters_used = 0
while True:
    try:
        driver.find_element(By.XPATH, '//button[@aria-label="Translate by voice" and @aria-pressed="false"]').click()
    except NoSuchElementException:
        print("aaaaaaaaaaaa 2: no button Translate by voice")
    except ElementClickInterceptedException as e:
        print("aaaaaaaaaaaa 21: can not click to button Translate by voice")
        print(e.args)
    except:
        traceback.print_exc()
    try:
        characters_used = driver.find_element(By.XPATH, '//span[text()="5,000"]/span').text
        characters_used = int(''.join(filter(str.isdigit, characters_used)))
        if characters_used > 650:
            try:
                # stop_voice_button = driver.find_element(By.XPATH, '//button[@aria-label="Stop translation by voice"]')
                # stop_voice_button.click()
                clear_source_text_button = driver.find_element(By.XPATH, '//button[@aria-label="Clear source text"]')
                clear_source_text_button.click()
            except NoSuchElementException:
                # print("aaaaaaaaaaaa 3: no button Stop translate by voice")
                print("aaaaaaaaaaaa 3: no button Clear source text")
            except:
                traceback.print_exc()
    except NoSuchElementException:
        print("aaaaaaaaaaaa 4: characters used element")
    except:
        traceback.print_exc()
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

# button Translate by voice
# <button class="VfPpkd-Bz112c-LgbsSe VfPpkd-Bz112c-LgbsSe-OWXEXe-e5LLRc-SxQuSe yHy1rc eT1oJ mN1ivc ZihNHd" jscontroller="soHxf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" data-disable-idom="true" disabled="" aria-label="Translate by voice"><div jsname="s3Eaab" class="VfPpkd-Bz112c-Jh9lGc"></div><div class="VfPpkd-Bz112c-J1Ukfc-LhBDec"></div><span class="" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" focusable="false" class=" NMm5M"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"></path><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"></path></svg></span><div class="VfPpkd-Bz112c-RLmnJb"></div></button>
# <button class="VfPpkd-Bz112c-LgbsSe VfPpkd-Bz112c-LgbsSe-OWXEXe-e5LLRc-SxQuSe yHy1rc eT1oJ mN1ivc ZihNHd NVubff" jscontroller="soHxf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" jsname="Sz6qce" data-disable-idom="true" aria-label="Translate by voice" aria-pressed="false" style="--mdc-ripple-fg-size: 24px; --mdc-ripple-fg-scale: 1.6666666666666667; --mdc-ripple-left: 8px; --mdc-ripple-top: 8px;"><div jsname="s3Eaab" class="VfPpkd-Bz112c-Jh9lGc"></div><div class="VfPpkd-Bz112c-J1Ukfc-LhBDec"></div><span class="" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" focusable="false" class="AeYb4d NMm5M"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"></path><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"></path></svg><div jscontroller="DFTXbf" data-progressvalue="0" class="DU29of a9u1Hb BbO7g"><div class="VfPpkd-JGcpL-Mr8B3-V67aGc" jsname="a2gnBb">Busy...</div><div class="VfPpkd-JGcpL-P1ekSe VfPpkd-JGcpL-P1ekSe-OWXEXe-A9y3zc" style="width: 24px; height: 24px;" role="progressbar" aria-label="Busy..." aria-hidden="true" jsname="LbNpof"><div class="VfPpkd-JGcpL-uI4vCe-haAclf"><svg class="VfPpkd-JGcpL-uI4vCe-LkdAo-Bd00G" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle class="VfPpkd-JGcpL-uI4vCe-u014N" cx="12" cy="12" r="8.75" stroke-width="2.5"></circle><circle class="VfPpkd-JGcpL-uI4vCe-LkdAo" jsname="MU5Wmf" cx="12" cy="12" r="8.75" stroke-dasharray="54.9778705" stroke-dashoffset="54.9778705" stroke-width="2.5"></circle></svg></div><div class="VfPpkd-JGcpL-IdXvz-haAclf"><div class="VfPpkd-JGcpL-QYI5B-pbTTYe"><div class="VfPpkd-JGcpL-lLvYUc-e9ayKc VfPpkd-JGcpL-lLvYUc-LK5yu"><svg class="VfPpkd-JGcpL-IdXvz-LkdAo-Bd00G" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="8.75" stroke-dasharray="54.9778705" stroke-dashoffset="27.48893525" stroke-width="2.5"></circle></svg></div><div class="VfPpkd-JGcpL-OcUoKf-TpMipd"><svg class="VfPpkd-JGcpL-IdXvz-LkdAo-Bd00G" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="8.75" stroke-dasharray="54.9778705" stroke-dashoffset="27.48893525" stroke-width="2"></circle></svg></div><div class="VfPpkd-JGcpL-lLvYUc-e9ayKc VfPpkd-JGcpL-lLvYUc-qwU8Me"><svg class="VfPpkd-JGcpL-IdXvz-LkdAo-Bd00G" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="8.75" stroke-dasharray="54.9778705" stroke-dashoffset="27.48893525" stroke-width="2.5"></circle></svg></div></div></div></div></div></span><div class="VfPpkd-Bz112c-RLmnJb"></div></button>

# characters used
# <span aria-label="1,290 of 5,000 characters used" role="img" class="ZTPlmc"><span jsname="qKMVIf">1,290</span> / 5,000</span>

# Clear source text
# <button class="VfPpkd-Bz112c-LgbsSe VfPpkd-Bz112c-LgbsSe-OWXEXe-e5LLRc-SxQuSe yHy1rc eT1oJ mN1ivc ZihNHd GA2I6e" jscontroller="soHxf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" jsname="X5DuWc" data-disable-idom="true" aria-label="Clear source text" style="--mdc-ripple-fg-size: 24px; --mdc-ripple-fg-scale: 1.6666666666666667; --mdc-ripple-left: 8px; --mdc-ripple-top: 8px;"><div jsname="s3Eaab" class="VfPpkd-Bz112c-Jh9lGc"></div><div class="VfPpkd-Bz112c-J1Ukfc-LhBDec"></div><i class="material-icons-extended VfPpkd-kBDsod" aria-hidden="true" lang="">clear</i><div class="VfPpkd-Bz112c-RLmnJb"></div></button>
