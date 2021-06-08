#!/bin/bash
if [ "$1" == "scan" ]; then
	python3 main.py scan
else
	current=$(gsettings get org.gnome.desktop.session idle-delay | awk -F' ' '{print $2}')
	python3 main.py start
	gsettings set org.gnome.desktop.session idle-delay ${current}
fi

