#!/bin/bash

# setup proxy for apt-get
# install necessary packages 
# setup proxy for bash commands
# install python packages using pip install
# reset proxy for apt-get

set_environment_variables () {
	echo "export http_proxy='http://172.16.0.2:3128/'" >> $HOME/.bashrc;
	echo "export https_proxy='http://172.16.0.2:3128/'" >> $HOME/.bashrc;
	echo "export ftp_proxy='http://172.16.0.2:3128/'" >> $HOME/.bashrc;
} 
installPackages () {
	sudo apt-get update;
	sudo apt-get install python-pip -y;
	sudo apt-get install vim -y;
	sudo apt-get install aptitude -y;
	sudo apt-get install cron -y;
}

installPythonAPI () {
	sudo pip install requests;
	#sudo pip install pushetta;
}

apt_setup () {
	echo "Acquire::http::Proxy 'http://172.16.0.2:3128/'" >> /etc/apt/apt.conf ;
	echo "Acquire::https::Proxy 'http://172.16.0.2:3128/'" >> /etc/apt/apt.conf ;
}

apt_reset (){
	echo "" > /etc/apt/apt.conf;
}


installPackages
installPythonAPI


sudo cp execute.py /
sudo cp launch.sh /
