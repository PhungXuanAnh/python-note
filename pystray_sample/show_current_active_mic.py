import time
from pystray import MenuItem as item 
import pystray 
from PIL import Image 
import pulsectl
from pulsectl import PulseVolumeInfo

pulse = pulsectl.Pulse('my-client-name')

def action(): 
    pass 
 
menu = (item('Action 1', action), item('Action 2', action)) 

ICON_MIC = {
    "built_in": Image.open("icon/mic_built_in.png"),
    "headphone_wire": Image.open("icon/mic_headphone_wire.png"),
    "headphone_blutooth1": Image.open("icon/mic_headphone_blutooth1.png"),
    "headphone_blutooth2": Image.open("icon/mic_headphone_blutooth2.png"),
    "orange_warning": Image.open("icon/orange_warning.jpg"),
    "all_muted": Image.open("icon/all_muted.png"),
}

icon = pystray.Icon("Test Icon 2", ICON_MIC["built_in"], "Test Icon 2", menu)
icon.run_detached()


MICROPHONES = {
    "built_in": "alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source",
    "headphone_wire": "alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__source",
    "headphone_blutooth1": "bluez_source.74_45_CE_22_CC_55.handsfree_head_unit",
    "headphone_blutooth2": "headphone_blutooth2",
}

def set_max_volume(source):
    volume = source.volume
    # print(volume.values) # list of per-channel values (floats)
    # print(volume.value_flat) # average level across channels (float)

    volume.value_flat = 1 # sets all volume.values to 1
    pulse.volume_set(source, volume) # applies the change

    n_channels = len(volume.values)
    new_volume = PulseVolumeInfo(1, n_channels) # 1 across all n_channels
    # new_volume = PulseVolumeInfo([0.15, 0.25]) # from a list of channel levels (stereo)
    pulse.volume_set(source, new_volume)

UNMUTE = 0

while True:
    current_icon = []
    
    opening_microphones = []
    for source in pulse.source_list():
        volumes = list(int(round(v*100)) for v in source.volume.values)
        
        if source.mute == UNMUTE:
            set_max_volume(source)
            
            if source.name == MICROPHONES["headphone_wire"]:
                current_icon.append(ICON_MIC["headphone_wire"])
                opening_microphones.append('headphone_wire')
            
            if source.name == MICROPHONES["built_in"]:
                current_icon.append(ICON_MIC["built_in"])
                opening_microphones.append('built_in')
            
            if source.name == MICROPHONES["headphone_blutooth1"]:
                current_icon.append(ICON_MIC["headphone_blutooth1"])
                opening_microphones.append('headphone_blutooth1')
            
            if source.name == MICROPHONES["headphone_blutooth2"]:
                current_icon.append(ICON_MIC["headphone_blutooth2"])
                opening_microphones.append('headphone_blutooth2')
                
    print("unmute microphones:", opening_microphones)
    
    if len(current_icon) > 1:
        current_icon = [ICON_MIC["orange_warning"]]
    if len(current_icon) < 1:
        current_icon = [ICON_MIC["all_muted"]]
        
    icon.icon = current_icon[0]
    time.sleep(0.5)
