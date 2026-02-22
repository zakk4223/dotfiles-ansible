#!/usr/bin/env python3

from collections import OrderedDict
import asyncio
import subprocess
import pulsectl_asyncio
import sys
import psutil
import i3ipc.aio
import i3ipc
import tomllib
import os
from i3ipc import Event



config_path = os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser("~"), ".config")), "pulse-autoswitch.toml")

config_data = {}

#only_displays = []
#an array that limits which displays to trigger audio switching for
#if this config option is missing, do it for all displays.
#can be either connector names "DP-1" or "<make> <model> <serial>" (probably what your compositor calls them)

#fallback_default = true
#if a window is MOVED to a display that isn't part of only_displays, switch the audio to the default sink

#sticky_sinks = []
#if any of the sinks in this array are currently the default sink, don't switch any audio
#use this if you don't want audio switching when your headphones are in use





with open(config_path, "rb") as f:
    config_data = tomllib.load(f)


i3_conn = i3ipc.Connection()

async def get_display_for_pid(pid, i3_conn):
    found_output = None
    i3_tree = await i3_conn.get_tree()
    pid_windows = i3_tree.find_by_pid(int(pid))
    for win in pid_windows:
        win_ws = win.workspace()
        if not win_ws:
            continue
        win_output = win_ws.ipc_data['output']
        print(f"PID {pid} has window on {win_output}")
        if found_output and win_output != found_output:
        #if the pid has multiple windows on different outputs, don't do anything
        #this means it is probably a bit flaky with things like firefox, which use process/thread pools 
        #that's fine, this is mostly for fullscreen games anyways
            return None
        found_output = win_output

    if not found_output:
        #process has no windows...
        return None

    all_outputs = await i3_conn.get_outputs()
    display_filter = config_data.get("only_displays")
    for output in all_outputs:
        if output.name == found_output:
            filter_string = f"{output.ipc_data['make']} {output.ipc_data['model']} {output.ipc_data['serial']}"
            if not display_filter:
                return output.model
            if filter_string in display_filter or output.name in display_filter:
                return output.model
    if config_data.get('fallback_default', True):
        return "@DEFAULT_SINK@" 
    return None



async def move_sources_for_pid(pid, pulse_con, i3ipc_con):

    pulse_server_info = await pulse_con.server_info()
    default_sink_name = pulse_server_info.default_sink_name
    sink_list = await pulse_con.sink_list()
    sticky_sinks = config_data.get('sticky_sinks', [])
    default_sink = None

    for sink in sink_list:
        if sink.name == default_sink_name:
                default_sink = sink
                break

    if default_sink and default_sink.description in sticky_sinks:
        return

     

    pid_display = await get_display_for_pid(pid, i3ipc_con)
    if not pid_display: 
        #steam big picture creates the sound stream from a process that has no windows, but the parent does.
        #just try the parent and see if that works. Might need to try the entire process group?
        try:
            c_process = psutil.Process(pid)
            pid_display = await get_display_for_pid(c_process.ppid(), i3ipc_con)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            #something went wrong, bail out.
            return
        if not pid_display:
            return

    sink_list = await pulse_con.sink_list()
    sink_inputs = await pulse_con.sink_input_list()

    target_sink = None
    print("PID DISPLAY ", pid_display)
    if pid_display == "@DEFAULT_SINK@":
        target_sink = default_sink
    else:
        for sink in sink_list:
            if sink.proplist['node.nick'] == pid_display:
                target_sink = sink
                break

    if not target_sink:
        return
    for sinp in sink_inputs:
        in_pid = int(sinp.proplist['application.process.id'])
        if (in_pid != pid):
            continue
        print(sinp.__dict__)
        print(target_sink.__dict__)
        in_sink = sinp.sink
        if target_sink:
            if in_sink != target_sink.index:
                await pulse_con.sink_input_move(sinp.index, target_sink.index)
                print(f"Moved input sink {in_sink} to sink {target_sink.name}")




async def i3_event_listen(pulse_con, i3ipc_con):
    async def on_new_window(self, ev):
        print("Got a new window for pid ", ev.container.pid)
        await move_sources_for_pid(ev.container.pid, pulse_con, i3ipc_con)

    async def on_move_window(self, ev):
        print("Got a move window for pid ", ev.container.pid)
        print(ev.container.ipc_data)
        await move_sources_for_pid(ev.container.pid, pulse_con, i3ipc_con)

    i3ipc_con.on(Event.WINDOW_NEW, on_new_window)
    i3ipc_con.on(Event.WINDOW_MOVE, on_move_window)
    await i3ipc_con.main()

async def pulse_event_listen(pulse_con, i3ipc_con):
    async for ev in pulse_con.subscribe_events('sink_input'):
        if ev.t == 'new':
            st_info = await pulse_con.sink_input_info(ev.index)
            st_pid = st_info.proplist['application.process.id']
            print("New Sink Input for PID ", st_pid)
            await move_sources_for_pid(int(st_pid), pulse_con, i3ipc_con)


async def main():
    pulse_con = pulsectl_asyncio.PulseAsync('pulse-switch-application-z')
    await pulse_con.connect()
    i3ipc_con = await i3ipc.aio.Connection().connect()
    
    pulse_task = asyncio.create_task(pulse_event_listen(pulse_con, i3ipc_con))
    i3_task = asyncio.create_task(i3_event_listen(pulse_con, i3ipc_con))
    await pulse_task
    await i3_task

asyncio.run(main())
