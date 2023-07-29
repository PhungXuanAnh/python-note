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
    "headphone_wire_analog": Image.open("icon/mic_headphone_wire.png"),
    "headphone_blutooth1": Image.open("icon/mic_headphone_blutooth1.png"),
    "headphone_blutooth2": Image.open("icon/mic_headphone_blutooth2.png"),
    "orange_warning": Image.open("icon/orange_warning.jpg"),
    "all_muted": Image.open("icon/all_muted.png"),
}

icon = pystray.Icon("Test Icon 2", ICON_MIC["built_in"], "Test Icon 2", menu)
icon.run_detached()


MICROPHONES = {
    "built_in": "alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source",
    "built_in_echo_cancel": "BuitIn_mic_EchoCancel",
    "headphone_wire": "alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__source",
    "headphone_wire_analog": "alsa_input.usb-Generic_USB_Audio_20210726905926-00.mono-fallback",
    "headphone_blutooth1": "bluez_source.74_45_CE_22_CC_55.handsfree_head_unit",
    "headphone_blutooth2": "headphone_blutooth2",
    "headphone_wire_echo_cancel": "WireHedset_mic_EchoCancel",
}

def set_volume(source, new_volume_number=1):
    current_volume = source.volume
    # print(volume.values) # list of per-channel values (floats)
    # print(volume.value_flat) # average level across channels (float)

    current_volume.value_flat = 1 # sets all volume.values to 1
    pulse.volume_set(source, current_volume) # applies the change

    n_channels = len(current_volume.values)
    # new_volume = PulseVolumeInfo(new_volume, n_channels) # 1 across all n_channels, max volume
    new_volume = PulseVolumeInfo(new_volume_number, n_channels)
    # new_volume = PulseVolumeInfo([0.15, 0.25]) # from a list of channel levels (stereo)
    pulse.volume_set(source, new_volume)

UNMUTE = 0

while True:
    opening_microphones = set()
    for source in pulse.source_list():
        volumes = list(int(round(v*100)) for v in source.volume.values)
        
        if source.mute == UNMUTE:
            if source.name == MICROPHONES["headphone_wire"] or source.name == MICROPHONES["headphone_wire_echo_cancel"]:
                opening_microphones.add('headphone_wire')
                set_volume(source, 0.77)
                
            if source.name == MICROPHONES["headphone_wire_analog"]:
                opening_microphones.add('headphone_wire_analog')
                set_volume(source, 1.53)
            
            if source.name == MICROPHONES["built_in"] or source.name == MICROPHONES["built_in_echo_cancel"]:
                opening_microphones.add('built_in')
                set_volume(source, 0.77)
            
            if source.name == MICROPHONES["headphone_blutooth1"]:
                opening_microphones.add('headphone_blutooth1')
                set_volume(source, 0.77)
            
            if source.name == MICROPHONES["headphone_blutooth2"]:
                opening_microphones.add('headphone_blutooth2')
                set_volume(source, 0.77)
                
    print("unmute microphones:", opening_microphones)
    
    if len(opening_microphones) == 2 and 'headphone_wire' in opening_microphones and 'headphone_wire_analog' in opening_microphones:
        icon.icon = ICON_MIC["headphone_wire"]
    elif len(opening_microphones) > 1:
        icon.icon = ICON_MIC["orange_warning"]
    elif len(opening_microphones) < 1:
        icon.icon = ICON_MIC["all_muted"]
    else:
        icon.icon = ICON_MIC[list(opening_microphones)[0]]
        
    time.sleep(0.5)
