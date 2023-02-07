'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "GUI for controlling robot from touchscreen input"
__version      = "1.0.1"
__status       = "Production"
__dependencies = "tkinter, global_params.py"
'''

import threading
import tkinter as tk
import tkinter.font as font
from PIL import ImageTk, Image
import glob 
import global_params

# threading
t = None

# gui visual params
background_color = '#4daff8'
button_color = '#ffffff'
highlight_color = '#f70103'
font_family = 'Quicksand Medium'

def appButton(root, button_text, button_icon, button_func, **kwargs):
    ''' APP BUTTONS
            
    '''

    size = kwargs.get('size', '')
    screen_width = root.winfo_screenwidth()
    font_size = int(0.05*screen_width)
    btn_height = int(font_size*3)
    btn_width = int(0.7*screen_width)
    
    if size == 'small':
        font_size = int(0.04*screen_width)
        btn_height = int(font_size*2.4)
        btn_width = int(0.5*root.winfo_screenwidth())

    return tk.Button(root, \
            text = button_text, \
            command = button_func, \
            bg = button_color, \
            activebackground = button_color, \
            activeforeground = highlight_color, \
            image = button_icon, \
            compound = tk.LEFT, \
            height = btn_height, \
            width = btn_width, \
            font = font.Font(family=font_family, size=font_size))

def btnImage(img_path, img_size):
    ''' ICON FOR APP BUTTONS
            
    '''
    
    btn_img = Image.open(img_path)
    btn_img = btn_img.resize((img_size,img_size))
    return ImageTk.PhotoImage(btn_img)
    
class appGUI(object):
    ''' TKINTER GUI
                
    '''

    def __init__(self, root):
        self.root = root
        root.configure(bg=background_color)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        font_size = int(0.04*screen_width)
        btn_icon_size = int(3*font_size)
    
        #### Status Buttons
        self.status_bar = tk.Frame(root)

        self.camera_status_label = tk.Label(self.status_bar, text=u"\u2b24", \
                                       bg=background_color)
        self.camera_status_label['font'] = font.Font(family=font_family, size=10)
        if global_params.camera_status:
            self.camera_status_label['fg'] = "#00FF00"
        else:
            self.camera_status_label['fg'] = "#FF0000"

        self.robot_status_label = tk.Label(self.status_bar, text=u"\u2b24", \
                                       bg=background_color)
        self.robot_status_label['font'] = font.Font(family=font_family, size=10)
        if global_params.robot_status:
            self.robot_status_label['fg'] = "#00FF00"
        else:
            self.robot_status_label['fg'] = "#FF0000"


        #### Return to Main Menu Button
        self.return_button_photo = btnImage('./rsc/img/icon_back.png', int(0.1*screen_width))
        self.return_button = appButton(root, \
                                       global_params.gui_lang["back"], \
                                       self.return_button_photo, \
                                       self.MainMenu, \
                                       size='small')
        
        #### Return to Settings Menu Button
        self.return_settings_button_photo = btnImage('./rsc/img/icon_back.png', int(0.1*screen_width))
        self.return_settings_button = appButton(root, \
                                                global_params.gui_lang["back"], \
                                                self.return_settings_button_photo, \
                                                self.SettingsMenu, \
                                                size='small')
        
        #### Start Button
        self.start_button_green_photo = btnImage('./rsc/img/icon_green.png', btn_icon_size)
        self.start_button_red_photo = btnImage('./rsc/img/icon_red.png', btn_icon_size)
        self.start_button = appButton(root, \
                                      global_params.gui_lang["start"], \
                                      self.start_button_green_photo, \
                                      lambda:self.StartStop(global_params.startFlag))
                                      
        #### Settings Menu Button
        self.settings_button_photo = btnImage('./rsc/img/icon_settings.png', btn_icon_size)
        self.settings_button = appButton(root, \
                                      global_params.gui_lang["settings"], \
                                      self.settings_button_photo, \
                                      self.SettingsMenu)
        
        #### Language Menu Button
        self.language_button_photo = btnImage('./rsc/img/icon_language.png', btn_icon_size)
        self.language_button = appButton(root, \
                                      global_params.gui_lang["language"], \
                                      self.language_button_photo, \
                                      self.LanguageMenu)
        
        #### Volume Menu Button
        self.volume_button_photo = btnImage('./rsc/img/icon_volume.png', btn_icon_size)
        self.volume_button = appButton(root, \
                                      global_params.gui_lang["volume"], \
                                      self.volume_button_photo, \
                                      self.VolumeMenu)
        
        #### Select Language 1 Button
        self.language_1_button_photo = btnImage('./rsc/img/1x1.png', 10)
        self.language_1_button = appButton(root, \
                                      "English", \
                                      self.language_1_button_photo, \
                                      lambda:self.getLanguageVal(0),\
                                      size='small')
        
        #### Select Language 2 Button
        self.language_2_button_photo = btnImage('./rsc/img/1x1.png', 10)
        self.language_2_button = appButton(root, \
                                      "中文", \
                                      self.language_2_button_photo, \
                                      lambda:self.getLanguageVal(1),\
                                      size='small')
        
        #### Display Language Selected Label
        self.lang_select_val = tk.StringVar()
        self.lang_select_val.set('Language Selected: ' + global_params.language)
        self.language_label = tk.Label(root, textvariable=self.lang_select_val, \
                                       bg=background_color)
        self.language_label['font'] = font.Font(family=font_family, size=int(0.8*font_size))

        #### Metronome Menu Button
        self.metronome_button_photo = btnImage('./rsc/img/icon_metronome.png', btn_icon_size)
        self.metronome_button = appButton(root, \
                                      global_params.gui_lang["metronome"], \
                                      self.metronome_button_photo, \
                                      self.MetronomeMenu)
        
        #### Metronome BPM Slider
        global metronome_val
        metronome_val = tk.IntVar()
        metronome_val.set(global_params.bpm)
        self.metronome_slider = tk.Scale(root, from_=30, to=170, tickinterval=140, resolution=1, \
                                         length=400, width=30, sliderlength=50, orient=tk.HORIZONTAL, \
                                         command=self.getMetronomeVal, variable=metronome_val, \
                                         bg=button_color)
        self.metronome_slider['font'] = font.Font(family=font_family, size=int(0.7*font_size))
        
        #### Metronome Play/Pause Button
        self.metronome_play_button_photo = btnImage('./rsc/img/icon_play.png', 2*btn_icon_size)
        self.metronome_pause_button_photo = btnImage('./rsc/img/icon_pause.png', 2*btn_icon_size)
        self.metronome_play_button = tk.Button(root, text='Play', \
                                               command=self.playMetronome, \
                                               bg=button_color, activebackground=button_color, activeforeground=highlight_color, \
                                               image=self.metronome_play_button_photo, highlightthickness=0, borderwidth=0)

        #### Sound Volume Slider
        global volume_val
        volume_val = tk.IntVar()
        volume_val.set(global_params.volume)
        self.volume_slider = tk.Scale(root, from_=0, to=100, tickinterval=10, resolution=10, orient=tk.HORIZONTAL, variable=volume_val, \
                                   command=self.getVolumeVal, length=400, width=30, sliderlength=50, \
                                   bg=button_color)
        self.volume_slider['font'] = font.Font(family=font_family, size=int(0.7*font_size))
        
        #### Sound Volume Icon
        self.volume_image_button_photo = btnImage('./rsc/img/icon_volume.png', 2*btn_icon_size)
        self.volume_image_button = tk.Button(root, text='Volume', \
                                             bg=button_color, activebackground=button_color, activeforeground=highlight_color, \
                                             image=self.volume_image_button_photo, highlightthickness=0, borderwidth=0)

        self.MainMenu()

    def MainMenu(self):
        ''' DISPLAY MAIN MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()

        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.status_bar.pack(side=tk.TOP, anchor=tk.NE)
        self.camera_status_label.pack(in_=self.status_bar, side=tk.LEFT)
        self.robot_status_label.pack(in_=self.status_bar, side=tk.LEFT)
        self.settings_button.pack(pady=5)
        self.metronome_button.pack(pady=10)
        self.start_button.pack(pady=10)

    def SettingsMenu(self):
        ''' DISPLAY SETTINGS MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()
        
        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.language_button.pack(pady=10)
        self.volume_button.pack(pady=10)
        self.return_button.pack(pady=10)
        
    def LanguageMenu(self):
        ''' DISPLAY LANGUAGE MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()
        
        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.language_1_button.pack(pady=10)
        self.language_2_button.pack(pady=10)
        self.language_label.pack(pady=10)
        self.return_settings_button.pack(pady=10)
        
    def VolumeMenu(self):
        ''' DISPLAY VOLUME MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()
        
        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.volume_image_button.pack(pady=10)
        self.volume_slider.pack(pady=10)
        self.return_settings_button.pack(pady=10)

    def MetronomeMenu(self):
        ''' DISPLAY METRONOME MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()

        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.metronome_play_button.pack(pady=10)
        self.metronome_slider.pack(pady=10)
        self.return_button.pack(pady=10)

    def RemoveAll(self):
        ''' REMOVE ALL GUI ELEMENTS CURRENTLY ON CANVAS
            
        '''
        
        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()

        element_list = [\
            self.status_bar,
            self.camera_status_label,
            self.robot_status_label,
            self.settings_button,
            self.start_button,
            self.language_button,
            self.volume_button,
            self.language_1_button,
            self.language_2_button,
            self.language_label,
            self.metronome_button,
            self.metronome_play_button,
            self.metronome_slider,
            self.volume_image_button,
            self.volume_slider,
            self.return_button,
            self.return_settings_button,
        ]

        for element in element_list:
            element.pack_forget()

    
    def StartStop(self, start_stop_flag):
        ''' START/STOP SESSION 
        Args:
            self                     : (Tkinter GUI object, required) 
            start_stop_flag          : (int, required)  Given session start/stop status.
        
        Returns:
            global_params.startFlag  : (bool)  Session start/stop status.
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()
        
        global t, camera
        start_stop_flag = global_params.startFlag
        if global_params.startFlag == 0:
            global_params.startFlag = 1
            
            ## disable settings button; unable to press
            self.settings_button.configure(state='disable')

            ## toggles start/stop button
            self.start_button.configure(image=self.start_button_red_photo, text=global_params.gui_lang["stop"])

            ## starts camera tracking and robot on separate thread
            global_params.stop_trackerFollower = False
            t = threading.Thread(target=global_params.trackerFollower, \
                                 args=(global_params.camera, global_params.camera_resolution, \
                                       global_params.robot, \
                                       global_params.cue, global_params.encouragement, \
                                       global_params.stop_trackerFollower, ) \
                                )
            t.start()

        else:
            global_params.startFlag = 0
            
            ## enable settings button; able to press
            self.settings_button.configure(state='normal')

            ## toggles start/stop button
            self.start_button.configure(image=self.start_button_green_photo, text=global_params.gui_lang["start"])
            
            ## stops camera tracking and robot, closes thread
            global_params.stop_trackerFollower = True
            t.join()            
        
        ## toggle status colors
        if global_params.camera_status:
            self.camera_status_label['fg'] = "#00FF00"
        else:
            self.camera_status_label['fg'] = "#FF0000"

        if global_params.robot_status:
            self.robot_status_label['fg'] = "#00FF00"
        else:
            self.robot_status_label['fg'] = "#FF0000"

        return global_params.startFlag 

    def getLanguageVal(self, lang_val):
        ''' GETS CURRENT GUI LANGUAGE VALUE
        Args:
            self                         : (Tkinter GUI object, required) 
            lang_val                     : (int, required)  Given integer corresponding to selected language.
        
        Returns:
            global_params.lang           : (int)   Integer corresponding to selected language.
            global_params.language       : (str)   Name of language.
            global_params.cue            : (str)   Path to audio cue files.
            global_params.encouragement  : (str)   Path to audio encouragement files.
            global_params.gui_lang       : (dict)  Dictionary that maps GUI elements to translated language.
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()

        lang = lang_val

        if lang == 0:
            global_params.cue = glob.glob('rsc/audio/en_cue-*.wav')
            global_params.encouragement = glob.glob('rsc/audio/en_encouragement-*.wav')
            
            global_params.language = 'ENGLISH'
            global_params.gui_lang = {
                "settings": "Settings",
                "language": "Language",
                "volume": "Volume",
                "metronome": "Metronome",
                "back": "Back",
                "start": "Start",
                "stop": "Stop"
            }
        elif lang == 1:
            global_params.cue = glob.glob('rsc/audio/cn_cue-*.wav')
            global_params.encouragement = glob.glob('rsc/audio/cn_encouragement-*.wav')
            
            global_params.language = '中文'
            global_params.gui_lang = {
                "settings": "设置",
                "language": "语言",
                "volume": "音量",
                "metronome": "节拍器",
                "back": "返回",
                "start": "开始",
                "stop": "停止"
            }

        ## changes gui elements to display in selected language
        self.settings_button.configure(text=global_params.gui_lang["settings"])
        self.language_button.configure(text=global_params.gui_lang["language"])
        self.volume_button.configure(text=global_params.gui_lang["volume"])
        self.start_button.configure(text=global_params.gui_lang["start"])
        self.metronome_button.configure(text=global_params.gui_lang["metronome"])
        self.return_button.configure(text=global_params.gui_lang["back"])
        self.return_settings_button.configure(text=global_params.gui_lang["back"])
        
        self.lang_select_val.set('Language Selected: ' + global_params.language)

        return global_params.lang, global_params.language, global_params.cue, global_params.encouragement, global_params.gui_lang

    def getMetronomeVal(self, arg):
        ''' GETS CURRENT METRONOME BPM VALUE
        Args:
            global_params.metronome_val  : (int, required)  Given current metronome BPM value from slider.
        
        Returns:
            global_params.bpm            : (int)  Current metronome BPM value.
        '''

        global metronome_val
        global_params.bpm = metronome_val.get()
        
        return global_params.bpm

    def playMetronome(self):
        ''' STARTS/STOPS PLAYING METRONOME
        Args:
            play_button_state  : (bool, required)  If metronome is currently playing or not.
        
        Returns:
            play_button_state  : (bool)  Updates if metronome is currently playing or not.
        '''

        ## Toggle metronome play status
        global_params.play_button_state = not global_params.play_button_state

        ## Update metronome play button display image and text
        if (global_params.play_button_state):
            self.metronome_play_button.configure(image=self.metronome_pause_button_photo)
            self.metronome_play_button['text'] = 'Pause'
        else:
            self.metronome_play_button.configure(image=self.metronome_play_button_photo)
            self.metronome_play_button['text'] = 'Play'

        return global_params.play_button_state

    def getVolumeVal(self, arg):
        ''' GETS CURRENT VOLUME LEVEL
        Args:
            global_params.volume_val  : (int, required)  Given current sound volume level from slider.
        
        Returns:
            global_params.volume      : (int)  Current sound volume level.
        '''

        global volume_val
        global_params.volume = volume_val.get()
        
        return global_params.volume

    def adjustVolume(self):
        ''' ADJUSTS VOLUME
        Args:
            volume      : (int, required)  Given sound volume level integer.
        
        Returns:
            
        '''

        global_params.speaker_mixer.setvolume(global_params.volume)
