#!/bin/bash

# exit when encounter error
set -e

# work in a temp dir
cd /tmp/

# download the script
wget -q https://raw.githubusercontent.com/czhang03/wifi_bt_auto_off/main/wifi_bt_auto_off.py

# move the script to autostart
mv ./wifi_bt_auto_off.py $HOME/.config/autostart/

# set the permission to executable
chmod u+x $HOME/.config/autostart/wifi_bt_auto_off.py

# start the script
$HOME/.config/autostart/wifi_bt_auto_off.py&

# final
echo "Success! The program is already running, and will auto start when you login."
echo "To stop the program, open system monitor, and kill 'wifi_bt_auto_off.py'."
echo "To delete the program, simply delete the script '~/.config/autostart/wifi_bt_auto_off.py'."
