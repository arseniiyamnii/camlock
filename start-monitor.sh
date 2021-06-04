#!/bin/bash
current=$(gsettings get org.gnome.desktop.session idle-delay | awk -F' ' '{print $2}')
python3 main.py
gsettings set org.gnome.desktop.session idle-delay ${current}
