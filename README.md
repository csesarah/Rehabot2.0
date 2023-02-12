# Rehabot2.0
### v1.1.0.20230210

---

## Quick Start
1. Simply flash the provided RPiOS image on to a microSD card
2. Robot will start when power is supplied to Raspberry Pi

Alternatively, follow the steps below to get started.

---

## Usage
On fresh install of Raspbian OS,

1. Configure Raspberry Pi settings

        sudo raspi-config

    a. Enable auto login on boot
      - **1 System Options** > **S5 Boot / Autologin** > **B2 Console Autologin**

    b. Enable Raspberry Pi Camera
      - **3 Interface Options** > **I1 Legacy Camera** > **Yes** > **Ok**

    c. Exit and do **not** reboot system 

2. Download repository

        git clone https://github.com/csesarah/Rehabot2.0 

3. Upload Arduino code 

4. For IMUs, remember to change ```00:00:00:00:00:00``` in ```appstart.sh``` to MAC addresses of bluetooth IMUs:
   
        sudo rfcomm bind rfcomm0 00:00:00:00:00:00
        sudo rfcomm bind rfcomm1 00:00:00:00:00:00

5. Pair bluetooth IMUs with the Bluetooth Manager on Raspberry Pi before continuing

6. Run ```install.sh``` to install all necessary prerequirements

                chmod +X install.sh
                ./install.sh

7. Reboot to autostart robot or run ```appstart.sh``` to start the robot

8. Robot moves when ArUco marker 0/1 is detected by Pi Camera