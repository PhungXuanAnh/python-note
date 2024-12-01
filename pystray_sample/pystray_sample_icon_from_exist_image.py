# https://pystray.readthedocs.io/en/latest/
# https://qr.ae/py5jTI

from pystray import MenuItem as item 
import pystray 
from PIL import Image 
 
def action(): 
    pass 
 
image = Image.open("icon/red_flower.jpeg") 
menu = (item('Action 1', action), item('Action 2', action)) 
icon = pystray.Icon("Test Icon 1", image, "Test Icon 1", menu) 
icon.run()
