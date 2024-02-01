#!/usr/bin/python3

import subprocess
import time
from typing import Optional
from enum import Enum

# whether to log debug messages
DEBUG = False
# kill wifi/bluetooth if not connected for this amount of time
KILL_TIMER = 10  # in seconds 
# the interval to check whether wifi/bluetooth is connected
CHECK_INTERVAL = 1  # in seconds

class Connections(Enum):
    WIFI = 0
    BLUETOOTH = 1

def is_connected(conn: Connections) -> bool:
    if conn == Connections.WIFI:
        wifi_check_res = subprocess.check_output(["nmcli", "connection", "show", "--active"]).decode('utf-8')
        return "wifi" in wifi_check_res
    elif conn == Connections.BLUETOOTH:
        bt_check_res = subprocess.check_output(["bluetoothctl", "devices", "Connected"]).decode('utf-8')
        return "Device" in bt_check_res

def kill(conn: Connections) -> bool:
    if conn == Connections.WIFI: 
        subprocess.run(["rfkill", "block", "wifi"])
    elif conn == Connections.BLUETOOTH:
        subprocess.run(["rfkill", "block", "bluetooth"])

def is_on(conn: Connections) -> bool:

    # check if the connection is soft blocked by rfkill
    if conn == Connections.WIFI:
        conn_check_res = subprocess.check_output(["rfkill", "list", "wifi", "--output", "soft"]).decode('utf-8')
        return "unblocked" in conn_check_res
    elif conn == Connections.BLUETOOTH:
        conn_check_res = subprocess.check_output(["rfkill", "list", "bluetooth", "--output", "soft"]).decode('utf-8')
        return "unblocked" in conn_check_res


# the input is a optional time
# if the input is a time, then it means the timer to disconnect is live
# otherwise, we are not counting to disconnect
# similarly for the output.
def check_to_kill(last_disconnect: Optional[float], 
                  conn: Connections) -> Optional[float]:
        
    # check if the connection is on or connected
    cur_on = is_on(conn)
    cur_connected = is_connected(conn)

    # dump debug information
    if DEBUG: 
        if last_disconnect == None:
            print(f"timer inactive for {conn.name}")
        else:
            print(f"{conn.name} timer active for {time.time() - last_disconnect} seconds")
        if cur_on:
            print(f"{conn.name} is on")
        else:
            print(f"{conn.name} is off")
        if cur_connected:
            print(f"{conn.name} is currently connected")
        else:
            print(f"{conn.name} is currently disconnected")

    # if the timer is off, and the connection is open and idle, start the timer
    if (last_disconnect == None 
            and cur_on 
            and not cur_connected):
        if DEBUG:
            print(f"{conn.name} disconnected, timer started")
        return time.time()  # start the countdown

    # if the timer is on, the device is currently on not connected,
    # and timer has exceeded the kill time, we will kill the connection
    elif (not last_disconnect == None 
            and cur_on
            and not cur_connected 
            and time.time() - last_disconnect > KILL_TIMER):
        if DEBUG:
            print(f"{conn.name} killed")
        kill(conn)
        return None  # stop the count down

    # timer is on, but the device has reconnected, we will turn off the timer
    elif (not last_disconnect == None 
            and (cur_connected or not cur_on)):
        if DEBUG:
            print(f"{conn.name} is reconnected, reset timer")
        return None

    # keep the countdown status
    else:
        return last_disconnect


# init no disconnection has been observed
bt_last_disconnect = None 
wifi_last_disconnect = None 
while True:
    # checking periodically 
    bt_last_disconnect = check_to_kill(bt_last_disconnect, Connections.BLUETOOTH) 
    wifi_last_disconnect = check_to_kill(wifi_last_disconnect, Connections.WIFI)
    time.sleep(CHECK_INTERVAL) 