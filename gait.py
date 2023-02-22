'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "Functions for calculating gait parameters"
__version      = "1.2.0"
__status       = "Production"
__dependencies = "pandas, scipy, global_params.py"
'''

import glob
import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, find_peaks
from ast import literal_eval

def vector_magnitude(data):
    ''' FIND VECTOR MAGNITUDE OF 3D VECTOR, V, WHERE V = (X, Y, Z)
    
    Args:
      data   : (arr,  required)  Given vector data.
    
    Returns:
      res    : (arr)  Vector magnitude.
    '''
    
    if len(data) == 0:
        return np.nan
    
    # magnitude = sqrt(x**2 + y**2 + z**2)
    res = np.sqrt(data[:,0]**2 + data[:,1]**2 + data[:,2]**2)
    return res

def butterworth(fc, fs, od, data):
    ''' BUTTERWORTH FILTER
    
    Args:
      fc     : (int,  required)  Given cutoff frequency.
      fs     : (int,  required)  Given sampling frequency.
      od     : (int,  required)  Given order of filter.
      data   : (arr,  required)  Given signal data.
    
    Returns:
      filtered_data  : (arr)  Filtered signal.
    '''
    
    [b,a] = butter(od,fc/(fs/2))
    filtered_data = lfilter(b,a,data)
    
    return filtered_data

def getCadenceStrideTime():
    ''' GET CADENCE AND STRIDE TIME FROM IMU OR CAMERA DATA
    
    '''

    ## get date
    if len(glob.glob('datafile.csv')) == 0:
        return 'NA', 'NA'
    else:
        try:
            data = pd.read_csv('datafile.csv', header=None)

            ## clean data
            tmp = []
            for i in range(0, len(data)):
                try:
                    if not ( isinstance(data.iloc[i,0],int) or \
                        isinstance(data.iloc[i,0],float) ):
                        tmp.append(i)
                except:
                    try:
                        if not ( isinstance( literal_eval(data.iloc[i,0]),int) or \
                            isinstance( literal_eval(data.iloc[i,0]),float)):
                            tmp.append(i)
                    except:
                        tmp.append(i)
           
            data = data.drop(tmp)

            ## assign data
            try:
                cam_data = data[data[2].isna()]
            except:
                return 'NA', 'NA'
            
            try:
                imu_data = data[~data[2].isna()]
                left_imu_data = imu_data[imu_data[1] == 0]
                right_imu_data = imu_data[imu_data[1] == 1]
            except:
                pass
        except:
             return 'NA', 'NA'

        # init params
        imu_cadence = None
        imu_stride_time = None
        cam_cadence = None
        cam_stride_time = None

    ## analyze camera data
    if len(cam_data) != 0:
        try:
            thres = 3

            tmp = []
            prev = None
            curr = None

            for i in range(0, len(cam_data)-1):
                if cam_data.iloc[i,1] == 0 and cam_data.iloc[i+1,1] == 1:
                    prev = i
                    prev_time = cam_data.iloc[i+1,0]
                
                if cam_data.iloc[i,1] == 1 and cam_data.iloc[i+1,1] == 0:
                    curr = i
                    curr_time = cam_data.iloc[i+1,0]
                    
                if prev != None and curr != None:
                    tmp.append([curr-prev, curr_time])
                    prev = None
                    curr = None
            tmp = np.array(tmp)
            tmp = tmp[tmp[:,0] >= thres]
            tmp = np.array(sorted(tmp, key=lambda x:x[1]))

            cam_stride_time = []
            if len(tmp) > 1:
                for i in range(0, len(tmp)-1):
                    cam_stride_time.append(tmp[i+1,1]-tmp[i,1])
                cam_stride_time = np.mean(cam_stride_time)
            else:
                cam_stride_time = None

            cam_cadence = len(tmp)
        except:
            pass

    ## analyze imu data
    def perLeg(data):
        fc = 2 # cutoff freq
        fs = 30 # sampling freq
        od = 2 # order
        filtered_data = butterworth(fc, fs, od, vector_magnitude(data.to_numpy()))
        
        peaks, _ = find_peaks(-filtered_data, prominence=15, distance=20)
        
        leg_imu_stride_time = []
        for i in range(0, len(peaks)-1):
            leg_imu_stride_time.append(peaks[i+1] - peaks[i])
            
        if len(leg_imu_stride_time) != 0:
            leg_imu_stride_time = np.mean(leg_imu_stride_time)
        else:
            leg_imu_stride_time = None
        
        if len(peaks) != 0:
            leg_imu_cadence = len(peaks)+1
        else:
            leg_imu_cadence = None
        
        return leg_imu_cadence, leg_imu_stride_time

    try:
        if len(left_imu_data) != 0:
            left_imu_cadence, left_imu_stride_time = perLeg(left_imu_data.iloc[:,2:5])
        else:
            left_imu_cadence, left_imu_stride_time = None, None
    except:
        left_imu_cadence, left_imu_stride_time = None, None
    try:
        if len(right_imu_data) != 0:
            right_imu_cadence, right_imu_stride_time = perLeg(right_imu_data.iloc[:,2:5])
        else:
            right_imu_cadence, right_imu_stride_time = None, None
    except:
        right_imu_cadence, right_imu_stride_time = None, None

    def getLegData(left, right):
        if left != None and right != None:
            return np.mean([left, right])
        elif left == None and right != None:
            return right
        elif left != None and right == None:
            return left
        else:
            return None

    imu_cadence = getLegData(left_imu_cadence, right_imu_cadence)
    imu_stride_time = getLegData(left_imu_stride_time, right_imu_stride_time)

    ## return cadence and stride time
    try:
        if imu_cadence != None and imu_stride_time != None:
            return int(imu_cadence), round(imu_stride_time,2)
        else:
            raise
    except:
        try:
            if cam_cadence != None and cam_stride_time != None:
                return int(cam_cadence), round(cam_stride_time,2)
            else:
                raise
        except:
            return 'NA', 'NA'