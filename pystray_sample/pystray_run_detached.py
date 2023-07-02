# https://pystray.readthedocs.io/en/latest/
# https://qr.ae/py5jTI
import time
from pystray import MenuItem as item 
import pystray 
from PIL import Image 
 
def action(): 
    pass 
 
menu = (item('Action 1', action), item('Action 2', action)) 
image = Image.open("icon/red_flower.jpeg") 
icon = pystray.Icon("Test Icon 1", image, "Test Icon 1", menu)
icon.run_detached()
# icon.stop()

while True:
    print("do something else in main thread")
    time.sleep(1)
