'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "Global parameters for Rehabot 2.0"
__version      = "1.0.1"
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
    global camera_status, robot_status, \
            camera, camera_resolution, \
            robot, trackerFollower, \
            play_button_state, startFlag, stop_trackerFollower, \
            bpm, lang, volume, language, gui_lang, lang, \
            cue, encouragement, beep, tick, mixer, speaker_mixer
    
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

    # initial flags
    play_button_state = False
    lang = 0
    startFlag = 0
    stop_trackerFollower = False
    
    # default language
    language = 'ENGLISH'
    gui_lang = {
        "settings": "Settings",
        "language": "Language",
        "volume": "Volume",
        "metronome": "Metronome",
        "back": "Back",
        "start": "Start",
        "stop": "Stop"
    }
    
    
