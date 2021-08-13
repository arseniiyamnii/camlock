if [ "$1" == "--uninstall" ]; then
	systemctl --user stop pycam.service
	systemctl --user disable pycam.service
	sudo rm /usr/bin/pycam.sh
	sudo rm /usr/bin/pycam-service
	sudo rm ~/.config/systemd/user/pycam.service
elif [ "$1" == "--hard" ]; then
	sudo touch ~/.owner.pickle
	sudo cp pycam.sh /usr/bin/pycam.sh
	sudo cp main.py /usr/bin/pycam-service
	mkdir -p ~/.config/systemd/user/
	sudo cp pycam.service ~/.config/systemd/user/pycam.service
	systemctl --user enable pycam.service
	systemctl --user start pycam.service
else
	sudo touch ~/.owner.pickle
	sudo ln pycam.sh /usr/bin/pycam.sh
	sudo ln main.py /usr/bin/pycam-service
	mkdir -p ~/.config/systemd/user/
	sudo ln pycam.service ~/.config/systemd/user/pycam.service
	systemctl --user enable pycam.service
	systemctl --user start pycam.service
fi
