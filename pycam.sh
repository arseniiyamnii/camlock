#!/bin/bash
pwd
cd "$(dirname "$0")"
if [ "$1" == "scan" ]; then
	python3 /usr/bin/pycam-service scan
else
	current=$(gsettings get org.gnome.desktop.session idle-delay | awk -F' ' '{print $2}')
	python3 /usr/bin/pycam-service
	gsettings set org.gnome.desktop.session idle-delay ${current}
fi

