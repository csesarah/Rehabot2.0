import cv2
import cv2.aruco as aruco
import time
import numpy as np
import glob
# from picamera.array import PiRGBArray
# from picamera import PiCamera
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
import time

camera = cv2.VideoCapture(0)
time.sleep(0.1)

def Calibrate():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Number of object points
    num_intersections_in_x = 4
    num_intersections_in_y = 4
    
    # Size of square in meters
    square_size = 0.011
    
    obj_points = []
    img_points = []
    
    object_points = np.zeros((num_intersections_in_x*num_intersections_in_y,3), np.float32)
    object_points[:,:2] = np.mgrid[0:num_intersections_in_x, 0:num_intersections_in_y].T.reshape(-1,2)
    object_points = object_points*square_size
    
        
    for i in range(0,9):
        img = cv2.imread('calib_img-%s.jpg' % i)
        img_size = (img.shape[1], img.shape[0])
        gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find chess board corners
        ret, corners = cv2.findChessboardCorners(gray_scale, (num_intersections_in_x, num_intersections_in_y), None)
        
        if ret:
            obj_points.append(object_points)
            
            corners_new = cv2.cornerSubPix(gray_scale,corners,(11,11),(-1,-1),criteria)
            img_points.append(corners)
            
            # Draw the corners
            drawn_img = cv2.drawChessboardCorners(img, (num_intersections_in_x,num_intersections_in_y), corners_new, ret)
            cv2.imwrite('calibration_img-%s.jpg' % i, drawn_img);

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, img_size, None, None)
    
    print('CALIBRATION COMPLETE\n')
    
    return [ret, mtx, dist, rvecs, tvecs]

def loadMtx(path):
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()
    cv_file.release()
    
    return [camera_matrix, dist_matrix]

###---------------------- CALIBRATION ---------------------------
# ret, mtx, dist, rvecs, tvecs = Calibrate()

# get calib mtx
[mtx, dist] = loadMtx('calib.txt')


###------------------ ARUCO TRACKER ---------------------------
# for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     frame = capture.array
        
    # operations on the frame
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 
#     # set dictionary size depending on the aruco marker selected
#     aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
# 
#     # detector parameters can be set here (List of detection parameters[3])
#     parameters = aruco.DetectorParameters_create()
#     parameters.adaptiveThreshConstant = 10
# 
#     # lists of ids and the corners belonging to each id
#     corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
# 
#     # font for displaying text (below)
#     font = cv2.FONT_HERSHEY_SIMPLEX
# 
#     # check if the ids list is not empty
#     # if no check is added the code will crash
#     if np.all(ids != None):
# 
#         # estimate pose of each marker and return the values
#         # rvet and tvec-different from camera coefficients
#         rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
#         #(rvec-tvec).any() # uncomment if numpy value array error
# 
#         for i in range(0, ids.size):
#             # draw axis for the aruco markers
#             aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)
# 
#         # draw a square around the markers
#         aruco.drawDetectedMarkers(frame, corners)
#         
#         # code to show ids of the marker found
#         strg = ''
#         for i in range(0, ids.size):
#             strg += str(ids[i][0])+', '
# 
#         cv2.putText(frame, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
#         
#     else:
#         # code to show 'No Ids' when no markers are found
#         cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    # display the resulting frame
#     cv2.imshow('frame',frame)
#     rawCapture.truncate(0)
    
    # terminate
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

while(True):        
        # read each frame from camera
#         frame = capture.array
        ret, frame = camera.read()
            
        # frame operations
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get aruco dict
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

        # detector parameters 
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10

        # detect aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # font for displaying text (below)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # check if the ids list is not empty
        # if no check is added the code will crash
        if np.all(ids != None):
            
            # estimate pose of each marker and return the values
            # rvet and tvec-different from camera coefficients
            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
            #(rvec-tvec).any() # uncomment if numpy value array error

            for i in range(0, ids.size):
             # draw axis for the aruco markers
             aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)
 
             # draw a square around the markers
             aruco.drawDetectedMarkers(frame, corners)
             
             # code to show ids of the marker found
             strg = ''
             for i in range(0, ids.size):
                 strg += str(ids[i][0])+', '
     
             cv2.putText(frame, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
             
            print(str(int(time.time()))+',1')

        else:
             # code to show 'No Ids' when no markers are found
             cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

             print(str(int(time.time()))+',0')

        # display the resulting frame
        cv2.imshow('frame',frame)
       
       # terminate
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

# When everything done, release the capture
cv2.destroyAllWindows()