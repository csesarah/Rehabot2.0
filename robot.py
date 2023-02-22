'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "Functions for wheeled robot ArUco marker follower with timed audio cues"
__version      = "1.2.0"
__status       = "Production"
__dependencies = "cv2, numpy, global_params.py"
'''

import cv2
import cv2.aruco as aruco
import numpy as np
from time import time
from random import randint
import global_params

def loadMtx(path):
    ''' GETS CALIBRATION MATRIX FROM .TXT FILE GENERATED FROM CV2 CALIBRATION
    Args:
            path :   (string, required) Given path to .txt containing calibration information.
    
    Returns:
            [camera_matrix, dist_matrix] :  (arr)
    '''

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()
    cv_file.release()

    return [camera_matrix, dist_matrix]

# get calib mtx
[mtx, dist] = loadMtx('calib.txt')

def trackerFollower_picamera(camera, camera_resolution, robot, cue, encouragement, stop_trackerFollower, sensitivity):
    ''' FUNCTION TO TRACK ARUCO MARKERS AND ACTIVATE GPIO ROBOT MOVEMENT 
    Args:
            camera                : (camera obj,   required) Either Pi camera or webcam object based on setting in main.py
            camera_resolution     : (arr of 2 int, required) Camera resolution in pixels
            robot                 : (robot obj,    required) GPIO robot created in main.py
            cue                   : (arr,          required) List of audio cue files available.
            encouragement         : (arr,          required) List of audio encouragment files available.
            stop_trackerFollower  : (bool,         required) Whether to stop camera tracking and robot
            sensitivity           : (int,          required) Sensitivity setting of robot
    '''
    
    # audio flags
    cue_play_flag = 0
    encouragement_play_flag = 0

    # timing
    stop_flag = 1
    robotStop_start_time = time() # start counting time when robot is stopped

    # main
    from picamera.array import PiRGBArray
    rawCapture = PiRGBArray(camera, size=(camera_resolution[0], camera_resolution[1]))

    SENSITIVITY = sensitivity * 10
    spd = 0 
    prev_robot_direction = None

    for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # read each frame from camera
        frame = capture.array

        if global_params.stop_trackerFollower:
            break

        if (cue_play_flag == 1):
            cue_play_flag = 0
            robotStop_start_time = time() # reset robotStop_start_time to 0

        if (encouragement_play_flag == 1):
            encouragement_play_flag = 0
            encouragement_start_time = time()

        # frame operations
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get aruco dict
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

        # detector parameters
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10

        # detect aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # check if the ids list is not empty if no check is added the code will crash
        if np.all(ids != None): # when marker is detected

            # estimate pose of each marker and return the values rvet and tvec-different from camera coefficients
            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

            # code to show ids of the marker found
            strg = ''
            for i in range(0, ids.size):
                strg += str(ids[i][0])+', '

            # robot
            stop_flag = 0
            robotStop_start_time = time() # reset robotStop_start_time to 0
            if (ids[i][0] == 0):
                robot.forward()
                prev_robot_direction = 0
            elif (ids[i][0] == 1):
                robot.backward()
                prev_robot_direction = 1

            print(str(time())+',1,,')

            spd = SENSITIVITY
        else: # when marker is not detected
            # robot
            if spd != 0:
                # move robot for every n frames after last detection of marker where n is function of sensitivity
                stop_flag = 0
                robotStop_start_time = time() # reset robotStop_start_time to 0
                if (prev_robot_direction == 0):
                    robot.forward()
                elif (prev_robot_direction == 1):
                    robot.backward()

                print(str(time())+',1,,')
                 
                spd -= 1
            else:
                stop_flag = 1
                robotStop_end_time = time()
                robotStop_time_elasped = robotStop_end_time - robotStop_start_time

                robot.stop()

                print(str(time())+',0,,')
                    

        # audio cues
        cue_time_thres = 3.0
        if (robotStop_time_elasped > cue_time_thres and stop_flag == 1):
            global_params.mixer.Sound(cue[randint(0, len(global_params.cue)-1)]).play()
            cue_play_flag = 1

        encouragement_time_thres = 1.0
        if (robotStop_time_elasped < encouragement_time_thres and stop_flag == 0):
            try:
                if (abs(encouragement_start_time - time()) > 3.0):
                    global_params.mixer.Sound(encouragement[randint(0, len(global_params.encouragement)-1)]).play()
                    encouragement_play_flag = 1
            except:
                global_params.mixer.Sound(encouragement[randint(0, len(global_params.encouragement)-1)]).play()
                encouragement_play_flag = 1

        # openCV truncate to prevent resolution buffer length error
        rawCapture.truncate(0)
        

def trackerFollower_webcam(camera, camera_resolution, robot, cue, encouragement, stop_trackerFollower, sensitivity):
    ''' FUNCTION TO TRACK ARUCO MARKERS AND ACTIVATE GPIO ROBOT MOVEMENT 
    Args:
            camera                : (camera obj,   required) Either Pi camera or webcam object based on setting in main.py
            camera_resolution     : (arr of 2 int, required) Camera resolution in pixels
            robot                 : (robot obj,    required) GPIO robot created in main.py
            cue                   : (arr,          required) List of audio cue files available.
            encouragement         : (arr,          required) List of audio encouragment files available.
            stop_trackerFollower  : (bool,         required) Whether to stop camera tracking and robot
            sensitivity           : (int,          required) Sensitivity setting of robot
    '''
    
    camera_resolution = camera_resolution

    # audio flags
    cue_play_flag = 0
    encouragement_play_flag = 0

    # timing
    stop_flag = 1
    robotStop_start_time = time() # start counting time when robot is stopped

    SENSITIVITY = sensitivity * 10
    spd = 0 
    prev_robot_direction = None

    while(True):
        # read each frame from camera
        ret, frame = camera.read()

        if global_params.stop_trackerFollower:
            break

        if (cue_play_flag == 1):
            cue_play_flag = 0
            robotStop_start_time = time() # reset robotStop_start_time to 0

        if (encouragement_play_flag == 1):
            encouragement_play_flag = 0
            encouragement_start_time = time()

        # frame operations
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get aruco dict
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

        # detector parameters
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10

        # detect aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # check if the ids list is not empty if no check is added the code will crash
        if np.all(ids != None):

            # estimate pose of each marker and return the values rvet and tvec-different from camera coefficients
            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

            # code to show ids of the marker found
            strg = ''
            for i in range(0, ids.size):
                strg += str(ids[i][0])+', '

            # robot
            stop_flag = 0
            robotStop_start_time = time() # reset robotStop_start_time to 0
            if (ids[i][0] == 0):
                robot.forward()
                prev_robot_direction = 0
            elif (ids[i][0] == 1):
                robot.backward()
                prev_robot_direction = 1

            print(str(time())+',1,,')

            spd = SENSITIVITY
        else: # when marker is not detected
            # robot
            if spd != 0:
                # move robot for every n frames after last detection of marker where n is function of sensitivity
                stop_flag = 0
                robotStop_start_time = time() # reset robotStop_start_time to 0
                if (prev_robot_direction == 0):
                    robot.forward()
                elif (prev_robot_direction == 1):
                    robot.backward()

                print(str(time())+',1,,')
                 
                spd -= 1
            else:
                stop_flag = 1
                robotStop_end_time = time()
                robotStop_time_elasped = robotStop_end_time - robotStop_start_time

                robot.stop()

                print(str(time())+',0,,')

        # audio cues
        cue_time_thres = 3.0
        if (robotStop_time_elasped > cue_time_thres and stop_flag == 1):
            global_params.mixer.Sound(cue[randint(0, len(global_params.cue)-1)]).play()
            cue_play_flag = 1

        encouragement_time_thres = 1.0
        if (robotStop_time_elasped < encouragement_time_thres and stop_flag == 0):
            try:
                if (abs(encouragement_start_time - time()) > 3.0):
                    global_params.mixer.Sound(encouragement[randint(0, len(global_params.encouragement)-1)]).play()
                    encouragement_play_flag = 1
            except:
                global_params.mixer.Sound(encouragement[randint(0, len(global_params.encouragement)-1)]).play()
                encouragement_play_flag = 1
