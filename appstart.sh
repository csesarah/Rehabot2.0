#!/bin/bash
sudo rfcomm bind rfcomm0 00:00:00:00:00:00
sudo rfcomm bind rfcomm1 00:00:00:00:00:00
cd /home/pi/Rehabot2.0
python3 main.py
