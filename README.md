WIFI BT Auto Off
---

A small utility to automatically turn off bluetooth and wifi on linux.
Inspired by the same functionality in [GrapheneOS](https://grapheneos.org/features#attack-surface-reduction)

## Install

#### Requirement

Python 3, nmcli, bluetoothctl, and rfkill;  
all of which are included in most Linux distro.

#### Manual

1. download `wifi_bt_auto_off.py`
1. Copy to `$HOME/.config/autostart`
1. Set it as executable by **right click > properties > Executable as Program**
1. restart the computer to start the script

## Config

At the start of the script there are couple constants:
```
# whether to log debug messages
DEBUG = False
# kill wifi/bluetooth if not connected for this amount of time
KILL_TIMER = 300  # in seconds 
# the interval to check whether wifi/bluetooth is connected
CHECK_INTERVAL = 15  # in seconds
```
By default, the wifi and bluetooth will turn off after 5 mins of inactivity,
and we will check the state of wifi and bluetooth every 15 second.

