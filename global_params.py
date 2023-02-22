'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "Global parameters for Rehabot 2.0"
__version      = "1.2.0"
__status       = "Production"
__dependencies = "pygame, alsaaudio" 
'''

import glob
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer
import alsaaudio

def init():
    ''' INITIALIZE GLOBAL PARAMETERS
            
    '''

    ## global parameters to be shared
    global camera_status, robot_status, imu1_status, imu2_status, \
            camera, camera_resolution, \
            robot, trackerFollower, \
            play_button_state, startFlag, stop_trackerFollower, \
            bpm, lang, volume, language, gui_lang, lang, \
            cue, encouragement, beep, tick, mixer, speaker_mixer, \
            recordIMU, stop_recordStream, \
            sensitivity_level
    
    # audio files
    cue = glob.glob('rsc/audio/en_cue-*.wav')
    encouragement = glob.glob('rsc/audio/en_encouragement-*.wav')
    tick = glob.glob('rsc/audio/tick.wav')[0]
    beep = glob.glob('rsc/audio/beep.wav')[0]
    
    # Speaker mixer for volume control
    speaker_mixer = alsaaudio.Mixer() 
    mixer.init()
    
    # initial metronome bpm setting
    bpm = 80

    # initial volume level setting
    volume = 100

    ## initial sensitivity setting
    sensitivity_level = 0

    # initial flags
    play_button_state = False
    lang = 0
    startFlag = 0
    stop_trackerFollower = False
    stop_recordStream = False
    
    # default language
    language = 'ENGLISH'
    gui_lang = {
                "settings" : "Settings",
                "language" : "Language",
                "records"  : "Records",
                "volume" : "Volume",
                "metronome" : "Metronome",
                "back" : "Back",
                "start" : "Start",
                "stop" : "Stop",
                "previous_session" : "Previous Session",
                "session_history" : "Session History",
                "delete" : "Delete",
                "session_date" : "Session Date\n(DD/MM/YYYY)",
                "duration": "Duration",
                "duration_units": "min",
                "cadence": "Cadence",
                "cadence_units": "steps/min",
                "stride_time": "Stride\nTime",
                "stride_time_units": "s",
                "sensitivity": "Speed",
                "sensitivity_desc": "Adjust robot speed",
            }
    