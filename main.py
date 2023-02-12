'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "Rehabot 2.0"
__version      = "1.1.0"
__status       = "Production"
__dependencies = "cv2, alsaaudio, gpiozero, tkinter, global_params.py, robot.py, gui.py"
'''

import tkinter as tk
import time
from gpiozero import Robot
import RPi.GPIO as GPIO
import cv2
import global_params
from gui import appGUI
from os import remove
from glob import glob
from serial import Serial
from serial.threaded import ReaderThread
from imu import SerialReaderProtocol, recordStream

## status
camera_status = False
robot_status = False
imu1_status = False
imu2_status = False

# robot
robot = Robot(left=(26,19), right=(13,6))
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.output(16, GPIO.LOW)
GPIO.output(20, GPIO.LOW)

# camera
camera_resolution = [640, 480]
camera_type = 1 # PiCamera: 0 | USB Webcam: 1
if camera_type == 0:
    try:
        from picamera import PiCamera
        camera = PiCamera()
        camera.resolution = (camera_resolution[0], camera_resolution[1])
        camera_status = True
    except:
        camera_status = False

    from robot import trackerFollower_picamera as trackerFollower
elif camera_type == 1:
    try:
        camera = cv2.VideoCapture(0)
        camera_status = True
    except:
        camera_status = False
    
    from robot import trackerFollower_webcam as trackerFollower
else:
    raise ValueError("Invalid camera type.")

# image params
if camera_status and camera_type == 0:
    center_image_x = camera.resolution[0] / 2
    center_image_y = camera.resolution[1] / 2

## bounding constants
#min_area = 300
#max_area = 70000
#bounding_const = [min_area, max_area]

#### Main
if __name__ == '__main__':
    global_params.init()
    if camera_status:
        global_params.camera = camera
        global_params.camera_resolution = camera_resolution
    
    if not robot_status:
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        robot_status = True

    if len(glob('datafile.csv')) > 0:
        remove('datafile.csv')

    try:
        serial_port_1 = Serial('/dev/rfcomm0', 115200, timeout=.1)
        reader_1 = ReaderThread(serial_port_1, SerialReaderProtocol)
        reader_1.start()
        imu1_status = True
    except:
        pass
    try:
        serial_port_2 = Serial('/dev/rfcomm1', 115200, timeout=.1)
        reader_2 = ReaderThread(serial_port_2, SerialReaderProtocol)
        reader_2.start()
        imu2_status = True
    except:
        pass

    global_params.camera_status = camera_status
    global_params.robot_status = robot_status
    global_params.imu1_status = imu1_status
    global_params.imu2_status = imu2_status
    global_params.robot = robot
    global_params.trackerFollower = trackerFollower
    global_params.recordStream = recordStream
    
    root = tk.Tk()
#    root.geometry('480x320')
    root.attributes('-fullscreen', True)
    appGUI = appGUI(root)
    
    run = True
    def update_run():
        global run
        run = False
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", update_run)
    
    while(run):
        root.update()

        ## metronome
        prev = time.perf_counter()
        delay = 60.0 / global_params.bpm
        if global_params.play_button_state:
            time.sleep(delay)
            curr = time.perf_counter()
            delta = curr - prev - delay
            delay -= delta

            global_params.mixer.Sound(global_params.tick).play()
