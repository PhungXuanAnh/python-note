# https://github.com/mk-fg/python-pulse-control/tree/master

import time
import pulsectl

pulse = pulsectl.Pulse('my-client-name')

def source_list():
    print(pulse.source_list())
    print(pulse.source_list()[0].__dict__)
    print("volume values:", pulse.source_list()[0].volume.__dict__)
    print("volumes:", list(int(round(v*100)) for v in pulse.source_list()[0].volume.values))
    for source in pulse.source_list():
        print("source name:", source.name)
        print("volumes:", list(int(round(v*100)) for v in source.volume.values))
        print("volume.value_flat", source.volume.value_flat)
        print("mute:", source.mute)

def sink_list():
    print(pulse.sink_list())
    sink = pulse.sink_list()[0]
    print(pulse.volume_change_all_chans(sink, -0.1))
    print(pulse.volume_set_all_chans(sink, 0.5))

def sink_input_list():
    # means playback
    print(pulse.sink_input_list())
    print(pulse.sink_input_list()[0].proplist)

def server_info():
    print(pulse.server_info().default_sink_name)
    # pulse.default_set(sink)

def card_list():
    card = pulse.card_list()[0]
    print(card.profile_list)
    # pulse.card_profile_set(card, 'output:hdmi-stereo')
    
def volume_set():
    """
        https://github.com/mk-fg/python-pulse-control/tree/master#volume
        this method can be able to set volume to: 
            PulseSinkInfo: self.sink_volume_set, (output device)
			PulseSinkInputInfo: self.sink_input_volume_set, (playback)
			PulseSourceInfo: self.source_volume_set, (input device)
			PulseSourceOutputInfo: self.source_output_volume_set (recording)
        the below example is for Sink input (playback volume)
    """
    from pulsectl import Pulse, PulseVolumeInfo

    with Pulse('volume-example') as pulse:
        sink_input = pulse.sink_input_list()[0] # first random sink-input stream

        volume = sink_input.volume
        print(volume.values) # list of per-channel values (floats)
        print(volume.value_flat) # average level across channels (float)

        time.sleep(1)

        volume.value_flat = 0.3 # sets all volume.values to 0.3
        pulse.volume_set(sink_input, volume) # applies the change

        time.sleep(1)

        n_channels = len(volume.values)
        new_volume = PulseVolumeInfo(0.5, n_channels) # 0.5 across all n_channels
        # new_volume = PulseVolumeInfo([0.15, 0.25]) # from a list of channel levels (stereo)
        pulse.volume_set(sink_input, new_volume)
        # pulse.sink_input_volume_set(sink_input.index, new_volume) # same as above

if __name__=='__main__':
    source_list()
    # sink_list()
    # sink_input_list()
    # sink_list()
    # server_info()
    # card_list()
    # volume_set()
