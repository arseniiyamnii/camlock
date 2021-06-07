#!/bin/bash
current=$(gsettings get org.gnome.desktop.session idle-delay | awk -F' ' '{print $2}')
python3 main.py start
gsettings set org.gnome.desktop.session idle-delay ${current}
