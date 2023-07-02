# https://github.com/mk-fg/python-pulse-control/tree/master

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

def sink_list():
    print(pulse.sink_list())
    sink = pulse.sink_list()[0]
    print(pulse.volume_change_all_chans(sink, -0.1))
    print(pulse.volume_set_all_chans(sink, 0.5))

def sink_input_list():
    print(pulse.sink_input_list())
    print(pulse.sink_input_list()[0].proplist)

def server_info():
    print(pulse.server_info().default_sink_name)
    # pulse.default_set(sink)

def card_list():
    card = pulse.card_list()[0]
    print(card.profile_list)
    # pulse.card_profile_set(card, 'output:hdmi-stereo')

if __name__=='__main__':
    source_list()
    # sink_list()
    # sink_input_list()
    # sink_list()
    # server_info()
    # card_list()
