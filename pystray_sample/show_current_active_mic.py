import time
from pystray import MenuItem as item 
import pystray 
from PIL import Image 
import pulsectl

pulse = pulsectl.Pulse('my-client-name')

def action(): 
    pass 
 
menu = (item('Action 1', action), item('Action 2', action)) 

ICON_MIC = {
    "wire": Image.open("icon/mic_headphone_wire.png"),
    "built_in": Image.open("icon/mic_built_in.png"),
    "virtual": '',
    "headphone_blutooth1": Image.open("icon/mic_headphone_blutooth1.png"),
    "headphone_blutooth2": Image.open("icon/mic_headphone_blutooth2.png"),
    "red_flower": Image.open("icon/red_flower.jpeg"),
}

icon = pystray.Icon("Test Icon 2", ICON_MIC["built_in"], "Test Icon 2", menu)
icon.run_detached()


MICROPHONES = {
    "wire": "alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__source",
    "built_in": "alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source",
    "virtual": "VirtualMicrophone",
    "headphone_blutooth1": "headphone_blutooth1",
    "headphone_blutooth2": "headphone_blutooth2",
}

  
while True:
    current_icon = []
    
    for source in pulse.source_list():
        volumes = list(int(round(v*100)) for v in source.volume.values)
        
        if source.volume.value_flat > 0.0:
            if source.name == MICROPHONES["wire"]:
                current_icon.append(ICON_MIC["wire"])
            
            if source.name == MICROPHONES["built_in"]:
                current_icon.append(ICON_MIC["built_in"])
            
            if source.name == MICROPHONES["headphone_blutooth1"]:
                current_icon.append(ICON_MIC["headphone_blutooth1"])
            
            if source.name == MICROPHONES["headphone_blutooth2"]:
                current_icon.append(ICON_MIC["headphone_blutooth2"])
    
    if len(current_icon) > 1:
        current_icon = [ICON_MIC["red_flower"]]
        
    icon.icon = current_icon[0]
    time.sleep(1)
