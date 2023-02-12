#!/bin/bash
echo -e "\n***************************************************\n*   __   ___            __   __  ___  __     __   *\n*  |__) |__  |__|  /\  |__) /  \  |   __|   |  |  *\n*  |  \ |___ |  | /--\ |__) \__/  |  |__  . |__|  *\n*                                                 *\n*  v1.1.0                                         *\n***************************************************\n\n"

echo -e "Installing required libraries ...\n"
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y nitrogen bluetooth bluez blueman libhdf5-dev libhdf5-serial-dev python3-pyqt5 libatlas-base-dev libjasper-dev python3-pil.imagetk libasound2-dev python3-scipy
sudo pip3 install --upgrade pip setuptools wheel numpy
sudo pip3 install pyalsaaudio opencv-python==4.5.3.56 opencv-contrib-python==4.5.3.56 pandas scipy 
echo -e "[SUCCESS]  Installed required libraries\n"

echo -e "Installing touchscreen driver ...\n"
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show
chmod +x LCD35B-show-V2
head -n -7 LCD35B-show-V2 > out.txt
sudo cp out.txt LCD35B-show-V2
./LCD35B-show-V2
cd ..
echo -e "[SUCCESS]  Installed touchscreen driver\n"

echo -e "Editing appstart.sh ...\n"
cwd=$(pwd)
sed -i "s,/home/pi,$cwd,g" appstart.sh
chmod +x appstart.sh
echo -e "[SUCCESS]  Edited appstart.sh\n"

echo -e "Editing /etc/xdg/openbox/autostart ...\n"
cwd=$(pwd)
sudo sh -c 'echo "nitrogen --set-scaled '$cwd'/rsc/img/wallpaper.png\nnitrogen --restore & \npulseaudio --start & \n'$cwd'/appstart.sh &" >> /etc/xdg/openbox/autostart'
echo -e "[SUCCESS]  Edited /etc/xdg/openbox/autostart\n"

echo -e "Editing /etc/rc.local ...\n"
(head -n -1 /etc/rc.local; echo -e "startx &\nexit 0") > out.txt
sudo cp out.txt /etc/rc.local
echo -e "[SUCCESS]  Edited /etc/rc.local\n"

echo -e "Editing /etc/X11/xinit/xinitrc ...\n"
(head -n -1 /etc/X11/xinit/xinitrc; echo -e "#. /etc/X11/xsession\nexec openbox-session") > out.txt
sudo cp out.txt /etc/X11/xinit/xinitrc
echo -e "[SUCCESS]  Edited /etc/X11/xinit/xinitrc\n"

echo -e "Editing /boot/config.txt ...\n"
sudo sh -c 'echo "gpio=6,13,19,26,16,20=op,dl,pd" >> /boot/config.txt'
echo -e "[SUCCESS]  Edited /boot/config.txt\n"

echo -e "Rebooting now ...\n"
sudo reboot
