'''
__author       = "Chen Si-En Sarah"
__copyright    = "Copyright 2021, Chen Si-En Sarah"
__email        = "chen.se.sarah@.gmail.com"

__description  = "OpenCV calibration for PiCamera"
__version      = "1.0.1"
__status       = "Production"
__dependencies = "numpy, cv2"
'''

import numpy as np
import glob
import cv2
import time
import pickle
import glob

def captureImages():
    print('CAPTURING IMAGES...') 
    
    # camera
    from picamera.array import PiRGBArray
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    time.sleep(0.1)

    for i in range(0, 10):
        camera.start_preview()
        time.sleep(5)
        camera.capture('calib_img-%s.jpg' % i)
        camera.stop_preview()
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print('IMAGES CAPTURE COMPLETE\n')
    

def Calibrate():
    print('CALIBRATION BEGIN\n')
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Number of object points
    num_intersections_in_x = 4
    num_intersections_in_y = 4
    
    # Size of square in meters
    square_size = 0.011
    
    # Arrays to store 3D points and 2D image points
    obj_points = []
    img_points = []
    
    object_points = np.zeros((num_intersections_in_x*num_intersections_in_y,3), np.float32)
    object_points[:,:2] = np.mgrid[0:num_intersections_in_x, 0:num_intersections_in_y].T.reshape(-1,2)
    object_points = object_points*square_size
    
    # No. of files
    filelist = len(glob.glob('calib_img-*.jpg'))
        
    for i in range(0, filelist):
        print('----- PROCESSING ' + str(i+1) + '/' + str(filelist) + ' -----')
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
            cv2.imwrite('calib_img-%s.jpg' % i, drawn_img);

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, img_size, None, None)
    
    print('CALIBRATION COMPLETE\n')
    
    return [ret, mtx, dist, rvecs, tvecs]


def saveMtx(mtx, dist, path):
    cv_file = cv2.FileStorage(path,cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    cv_file.release()
    
def loadMtx(path):
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()
    cv_file.release()
    
    return [camera_matrix, dist_matrix]


if __name__ == "__main__":
    captureImages()    

    ret, mtx, dist, rvecs, tvecs = Calibrate()
    saveMtx(mtx, dist, 'calib.txt')
    
    [mtx, dist] = loadMtx('calib.txt')
    print(mtx)
    print(dist)
    