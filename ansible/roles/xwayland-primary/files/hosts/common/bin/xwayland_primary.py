#!/usr/bin/env python3

import asyncio
import subprocess
import sys
import psutil
import i3ipc
import tomllib
import os
import subprocess
from i3ipc import Event



config_path = os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser("~"), ".config")), "xwayland-primary.toml")

config_data = {}


#This script will likely keep xwayland alive forever.
#if you're using a config where you want Xwayland to be started on demand, this script will generate that demand.
#maybe there's a way to not do this, but I'm not motivated enough to figure it out. 


#primary_display = DP-1 
#The default primary display. 
#can be either connector names "DP-1" or "<make> <model> <serial>" (probably what your compositor calls them)

#follow_displays = []
#when an output in this array gets focus, the xwayland primary will switch to it.
#if this array is empty, the display is ALWAYS set to the primary_display on focus.
    

#fallback_default = true
#there are multiple modes of operation:
#1)
#follow_displays is empty and fallback_default is false - 
#set the primary to the currently focused display unconditionally. 
#2)
#follow_displays is empty and fallback_default is true - 
#reassert primary display every workspace focus change.
#3)
#follow_displays is populated and fallback_default is false - 
#if the focused output is in this list, set it to the primary
#otherwise, don't change anything.
#4)
#follow displays is populated and fallback_default is true
#if the focused output is in this list, set it to the primary
#otherwise, don't set primary_display as primary




try:
    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)
except FileNotFoundError:
    config_data = {}






def set_display_primary(output):
    print(f"Set primary to {output.name}")
    subprocess.run(['xrandr', '--output', output.name, '--primary'])
    return None

def match_display_names(display_names, output):
    #connector name
    if output.name in display_names:
        return True
    #long name
    long_name =  f"{output.make} {output.model} {output.serial}"
    if long_name in display_names:
        return True
    return False


def handle_output_focus(i3ipc_con, output_name):
    default_output = None
    outputs = i3ipc_con.get_outputs()
    focused_output = None
    for output in outputs:
        if output.name == output_name:
            focused_output = output
        if match_display_names([config_data.get('primary_display', "DP-1")], output):
            default_output = output


    if focused_output:
        follow_displays = config_data.get('follow_displays', [])
        if len(follow_displays):
            if match_display_names(follow_displays, focused_output):
                set_display_primary(focused_output)
            elif config_data.get('fallback_default', None) and default_output:
                set_display_primary(default_output)
        else:
            if (config_data.get('fallback_default', False)):
                set_display_primary(default_output)
            else:
                set_display_primary(focused_output)

            









def i3_event_listen(i3ipc_con):
    def on_workspace_focus(self, ev):
        ws_output = ev.current.ipc_data['output']
        handle_output_focus(i3ipc_con, ws_output)

    i3ipc_con.on(Event.WORKSPACE_FOCUS, on_workspace_focus)
    i3ipc_con.main()



def main():
    i3ipc_con = i3ipc.Connection()
    for output in i3ipc_con.get_outputs():
        if output.ipc_data['focused']:
            handle_output_focus(i3ipc_con, output.name)
    i3_event_listen(i3ipc_con)


main()
