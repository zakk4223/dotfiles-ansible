#!/usr/bin/env python3

from collections import OrderedDict
import subprocess
import pulsectl
import sys



pulse = pulsectl.Pulse('pulse-sink-toggle-z')

sink_names = sys.argv[1:]
if not len(sink_names):
    sink_names = ["Audeze Maxwell Game", "AudioBox Go Analog Stereo", "Navi 21/23 HDMI/DP Audio Controller (SAMSUNG)"] 
#pa_sink_desc_map = OrderedDict(zip(sink_names, [None]*len(sink_names))) 

def switch_default_sink(sink_info):
    print(f"SWITCHING TO {sink_info}")
    pulse.default_set(sink_info)
    subprocess.run(["notify-send", sink_info.description])
    sys.exit()

pa_sink_desc_map = {}

pulse_server_info = pulse.server_info()
pulse_default_sink_name = pulse_server_info.default_sink_name


for pa_sink in pulse.sink_list():
    if pa_sink.description in sink_names:
        is_default = True if pulse_default_sink_name == pa_sink.name else False 
        pa_sink_desc_map[pa_sink.description] = [pa_sink, is_default]



print(pa_sink_desc_map)

found_def=False
for sink_desc in sink_names:
    print(f"Trying {sink_desc}")
    if sink_desc not in pa_sink_desc_map: continue
    sink_info = pa_sink_desc_map[sink_desc]
    if found_def: #we found the default sink on the last iteration, now set to the 'next' one
        switch_default_sink(sink_info[0])
    if sink_info and sink_info[1]:
        print(f"{sink_desc} is default")
        found_def=True

if found_def:
    #find first available one 
    for sink_desc in sink_names:
        if sink_desc not in pa_sink_desc_map: continue
        sink_info = pa_sink_desc_map[sink_desc]
        if sink_info and sink_info[0]:
          switch_default_sink(sink_info[0])




