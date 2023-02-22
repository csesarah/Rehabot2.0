'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "GUI for controlling robot from touchscreen input"
__version      = "1.2.0"
__status       = "Production"
__dependencies = "tkinter, global_params.py"
'''

import threading
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from PIL import ImageTk, Image
import glob 
from datetime import datetime
from time import mktime
import csv
from ast import literal_eval
import global_params
from gait import getCadenceStrideTime

# threading
t = None
s = None

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
    btn_height = int(font_size*2.2)
    btn_width = int(0.7*screen_width)
    
    if size == 'small':
        font_size = int(0.04*screen_width)
        btn_height = int(font_size*2.4)
        btn_width = int(0.5*root.winfo_screenwidth())

    if size == 'xsmall':
        font_size = int(0.02*screen_width)
        btn_height = int(font_size)
        btn_width = int(0.1*root.winfo_screenwidth())

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

def convertToUnixTime(val):
    ''' CONVERT DATETIME STRING TO UNIX TIME

    '''

    try:
        return str(mktime(datetime.strptime(val, "%d/%m/%Y  %I:%M %p").timetuple()))
    except:
        return val

def statusIndicators(root):
    ''' GREEN/RED STATUS CIRCLE ICONS ON MAIN MENU

    '''
    return tk.Label(root,\
                    text=u"\u2b24", \
                    bg=background_color, \
                    font = font.Font(family=font_family, size=10))

def toggle_status_color(status, label):
    ''' CHANGES COLOR OF STATUS CIRCLE ICONS ON MAIN MENU
            Green if component is in working condition, else
            red if component is not working

    '''
    if status:
        label.configure(fg="#00FF00")
    else:
        label.configure(fg="#FF0000")


class appGUI(object):
    ''' TKINTER GUI
                
    '''

    def __init__(self, root):
        self.root = root
        root.configure(bg=background_color)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        font_size = int(0.04*screen_width)
        btn_icon_size = int(2.5*font_size)
    
        #### Status Buttons
        self.status_bar = tk.Frame(root)

        self.camera_status_label = statusIndicators(self.status_bar)
        toggle_status_color(global_params.camera_status, self.camera_status_label)

        self.robot_status_label = statusIndicators(self.status_bar)
        toggle_status_color(global_params.robot_status, self.robot_status_label)

        self.imu1_status_label = statusIndicators(self.status_bar)
        toggle_status_color(global_params.imu1_status, self.imu1_status_label)

        self.imu2_status_label = statusIndicators(self.status_bar)
        toggle_status_color(global_params.imu2_status, self.imu2_status_label)

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
        
        #### Records Menu Button
        self.records_button_photo = btnImage('./rsc/img/icon_records.png', btn_icon_size)
        self.records_button = appButton(root, \
                                      global_params.gui_lang["records"], \
                                      self.records_button_photo, \
                                      self.RecordsMenu)

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
        
        #### Sensitivity Menu Button
        self.sensitivity_button_photo = btnImage('./rsc/img/icon_sensitivity.png', btn_icon_size)
        self.sensitivity_button = appButton(root, \
                                      global_params.gui_lang["sensitivity"], \
                                      self.sensitivity_button_photo, \
                                      self.SensitivityMenu)
        
        #### Sensitivity Setting
        self.sensitivity_setting = tk.Frame(root, bg=background_color)

        #### Decrease Sensitivity Button
        self.sensitivity_decrease_button_photo = btnImage('./rsc/img/1x1.png', 10)
        self.sensitivity_decrease_button = tk.Button(root, \
            text = "-", \
            command = self.DecreaseSensitivity, \
            bg = button_color, activebackground = button_color, activeforeground = highlight_color, \
            image = self.sensitivity_decrease_button_photo, compound = tk.LEFT, \
            height = 3*font_size, \
            width = font_size*3, \
            font = font.Font(family=font_family, size=2*font_size))
        
        #### Increase Sensitivity Button
        self.sensitivity_increase_button_photo = btnImage('./rsc/img/1x1.png', 10)
        self.sensitivity_increase_button = tk.Button(root, \
            text = "+", \
            command = self.IncreaseSensitivity, \
            bg = button_color, activebackground = button_color, activeforeground = highlight_color, \
            image = self.sensitivity_increase_button_photo, compound = tk.LEFT, \
            height = 3*font_size, \
            width = font_size*3, \
            font = font.Font(family=font_family, size=2*font_size))
        
        #### Display Sensitivity Level Label
        self.sensitivity_level_val = tk.StringVar()
        self.sensitivity_level_val.set(str(global_params.sensitivity_level+1))
        self.sensitivity_level_label = tk.Label(root, textvariable=self.sensitivity_level_val, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(4*font_size)))

        #### Display Sensitivity Level Label
        self.sensitivity_desc_val = tk.StringVar()
        self.sensitivity_desc_val.set(global_params.gui_lang["sensitivity_desc"])
        self.sensitivity_desc_label = tk.Label(root, textvariable=self.sensitivity_desc_val, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.8*font_size)))

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
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.8*font_size)))

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
                                         bg=button_color, font = font.Font(family=font_family, size=int(0.7*font_size)))
        
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
                                   bg=button_color, font = font.Font(family=font_family, size=int(0.7*font_size)))
        
        #### Sound Volume Icon
        self.volume_image_button_photo = btnImage('./rsc/img/icon_volume.png', 2*btn_icon_size)
        self.volume_image_button = tk.Button(root, text='Volume', \
                                             bg=button_color, activebackground=button_color, activeforeground=highlight_color, \
                                             image=self.volume_image_button_photo, highlightthickness=0, borderwidth=0)

        #### Records Previous Session Information
        self.prev_session_info_1 = tk.Frame(root, bg=background_color)
        self.prev_session_info_2 = tk.Frame(root, bg=background_color)
        self.session_history = tk.Frame(root, bg=background_color)

        #### Records Previous Session Label
        self.previous_session_label_txt = tk.StringVar()
        self.previous_session_label_txt.set(global_params.gui_lang["previous_session"])
        self.records_previous_session_label = tk.Label(root, textvariable=self.previous_session_label_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.7*font_size), underline=True))

        #### Records Previous Session Duration Label
        self.duration_label_txt = tk.StringVar()
        self.duration_label_txt.set(global_params.gui_lang["duration"]+3*" ")
        self.records_previous_session_duration_label = tk.Label(self.prev_session_info_1, textvariable=self.duration_label_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.6*font_size)))

        #### Records Previous Session Cadence Label
        self.cadence_label_txt = tk.StringVar()
        self.cadence_label_txt.set(global_params.gui_lang["cadence"]+3*" ")
        self.records_previous_session_cadence_label = tk.Label(self.prev_session_info_2, textvariable=self.cadence_label_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.6*font_size)))

        #### Records Previous Session Stride Time Label
        self.stride_time_label_txt = tk.StringVar()
        self.stride_time_label_txt.set(global_params.gui_lang["stride_time"].replace('\n',' ')+3*" ")
        self.records_previous_session_stride_time_label = tk.Label(self.prev_session_info_2, textvariable=self.stride_time_label_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.6*font_size)))

        ## Previous Session Start/Stop Time
        self.prev_session_start_time = 0
        self.prev_session_stop_time = 0
        
        #### Records Session History Label
        self.session_history_label_txt = tk.StringVar()
        self.session_history_label_txt.set(global_params.gui_lang["session_history"])
        self.records_session_history_label = tk.Label(root, textvariable=self.session_history_label_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.6*font_size)))

        #### Records Table
        self.records_table_wrapper = tk.Frame(root)
        self.style = ttk.Style(root)
        self.style.configure('Treeview', rowheight=40)
        self.records_table_scrollbar = tk.Scrollbar(self.records_table_wrapper,width=25)
        self.records_table = ttk.Treeview(self.records_table_wrapper, yscrollcommand=self.records_table_scrollbar.set, height=2)
        self.records_table_scrollbar.config(command=self.records_table.yview)        

        self.records_table['columns'] = ('num', 'session_datetime', 'session_duration', 'cadence', 'stride_time')

        self.records_table.column("#0", width=0, stretch=tk.NO)
        self.records_table.column("num", anchor=tk.CENTER, width=30)
        self.records_table.column("session_datetime", anchor=tk.CENTER, width=160)
        self.records_table.column("session_duration", anchor=tk.CENTER, width=75)
        self.records_table.column("cadence", anchor=tk.CENTER, width=90)
        self.records_table.column("stride_time", anchor=tk.CENTER, width=75)

        self.records_table.heading("#0",text="\n")
        self.records_table.heading("num",text="\n")
        self.records_table.heading("session_datetime",text=global_params.gui_lang["session_date"]+"\n")
        self.records_table.heading("session_duration",text=global_params.gui_lang["duration"]+"\n("+global_params.gui_lang["duration_units"]+")")
        self.records_table.heading("cadence",text=global_params.gui_lang["cadence"]+"\n("+global_params.gui_lang["cadence_units"]+")")
        self.records_table.heading("stride_time",text=global_params.gui_lang["stride_time"]+" ("+global_params.gui_lang["stride_time_units"]+")")

        ## read records from csv file
        self.records_list = []
        with open('records.csv', 'r') as records_csv:
            data = csv.reader(records_csv, delimiter=",")
            self.records_list.append(next(data))
        self.records_list = self.records_list[0]
        for i in range(0, len(self.records_list)):
            self.records_list[i] = literal_eval(self.records_list[i])

        ## insert records from csv file into table
        for i in range(0, len(self.records_list)):
            self.records_table.insert(parent='',index='end',iid=i,text='',values=self.records_list[i])

        #### Delete Records Button
        self.delete_records_button_photo = btnImage('./rsc/img/1x1.png', 10)
        self.delete_records_button = appButton(root, \
                                      global_params.gui_lang['delete'], \
                                      self.delete_records_button_photo, \
                                      self.DeleteRecords,\
                                      size='xsmall')

        #### Records Previous Session Datetime
        self.datetime_val = self.records_list[0][1]
        self.datetime_txt = tk.StringVar()
        self.datetime_txt.set(self.datetime_val)
        self.records_previous_session_datetime = tk.Label(self.prev_session_info_1, textvariable=self.datetime_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.8*font_size), weight='bold'))

        #### Records Previous Session Duration
        self.duration_val = self.records_list[0][2]
        self.duration_txt = tk.StringVar()
        self.duration_txt.set(self.duration_val + ' ' + global_params.gui_lang['duration_units'])
        self.records_previous_session_duration = tk.Label(self.prev_session_info_1, textvariable=self.duration_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.7*font_size), weight='bold'))

        #### Records Previous Session Cadence
        self.cadence_val = self.records_list[0][3]
        self.cadence_txt = tk.StringVar()
        self.cadence_txt.set(self.cadence_val + ' ' + global_params.gui_lang['cadence_units'])
        self.records_previous_session_cadence = tk.Label(self.prev_session_info_2, textvariable=self.cadence_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.7*font_size), weight='bold'))

        #### Records Previous Session Stride Time
        self.stride_time_val = self.records_list[0][4]
        self.stride_time_txt = tk.StringVar()
        self.stride_time_txt.set(self.stride_time_val + ' ' + global_params.gui_lang['stride_time_units'])
        self.records_previous_session_stride_time = tk.Label(self.prev_session_info_2, textvariable=self.stride_time_txt, \
                                       bg=background_color, font = font.Font(family=font_family, size=int(0.7*font_size), weight='bold'))

        #### Line Separator
        self.separator = ttk.Separator(root, orient='horizontal')

        #### Initialize with Main Menu
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
        self.imu1_status_label.pack(in_=self.status_bar, side=tk.LEFT)
        self.imu2_status_label.pack(in_=self.status_bar, side=tk.LEFT)

        self.settings_button.pack(pady=2)
        self.records_button.pack(pady=5)
        self.metronome_button.pack(pady=5)
        self.start_button.pack(pady=5)

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
        self.sensitivity_button.pack(pady=10)
        self.return_button.pack(pady=10)

    def RecordsMenu(self):
        ''' DISPLAY RECORDS MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()
        
        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.records_previous_session_label.pack(side=tk.TOP, anchor=tk.NW, padx=10)
        self.prev_session_info_1.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=True, padx=10)
        self.prev_session_info_2.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=True, padx=10)
        
        self.records_previous_session_datetime.pack(in_=self.prev_session_info_1, side=tk.LEFT, fill=tk.BOTH)
        
        self.records_previous_session_duration.pack(in_=self.prev_session_info_1, side=tk.RIGHT, fill=tk.BOTH)
        self.records_previous_session_duration_label.pack(in_=self.prev_session_info_1, side=tk.RIGHT, fill=tk.BOTH)
        
        self.records_previous_session_cadence_label.pack(in_=self.prev_session_info_2, side=tk.LEFT, fill=tk.BOTH)
        self.records_previous_session_cadence.pack(in_=self.prev_session_info_2, side=tk.LEFT, fill=tk.BOTH)
        
        self.records_previous_session_stride_time.pack(in_=self.prev_session_info_2, side=tk.RIGHT, fill=tk.BOTH)
        self.records_previous_session_stride_time_label.pack(in_=self.prev_session_info_2, side=tk.RIGHT, fill=tk.BOTH)

        self.separator.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.session_history.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=True, padx=10)
        self.records_session_history_label.pack(in_=self.session_history, side=tk.LEFT, fill=tk.BOTH)
        self.delete_records_button.pack(in_=self.session_history, side=tk.RIGHT, fill=tk.BOTH)

        self.records_table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_table_wrapper.pack(pady=10)
        self.records_table.pack()

        self.return_button.pack(pady=5)
    
    def DeleteRecords(self):
        ''' DELETE ALL SESSION RECORDS
            
        '''
        
        ## re-initialize records list
        self.records_list = []
        for i in range(0,8):
            self.records_list.append((str(i+1), '-', '-', '-', '-'))

        ## refresh records table
        self.RefreshRecords(self.records_list)

    def RefreshRecords(self, records_list):
        ''' REFRESH RECORDS TABLE
            
        '''
        ## delete all existing records
        for i in self.records_table.get_children():
            self.records_table.delete(i)

        ## insert records into records table
        for i in range(0, len(self.records_list)):
            self.records_table.insert(parent='',index='end',iid=i,text='',values=self.records_list[i])

        ## reset records table
        self.RecordsMenu

        ## update records csv file
        with open('records.csv', 'w') as records_csv:
            writer = csv.writer(records_csv)
            writer.writerow(self.records_list)
            records_csv.close()

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

    def SensitivityMenu(self):
        ''' DISPLAY SENSITIVITY MENU ON CANVAS
            
        '''

        ## play beep when screen changes
        global_params.mixer.Sound(global_params.beep).play()
        
        ## remove all gui elements currently on screen
        self.RemoveAll()

        ## menu gui elements
        self.sensitivity_desc_label.pack(side=tk.TOP, padx=10, pady=10)
        self.sensitivity_setting.pack(side=tk.TOP, padx=10, pady=10)
        self.sensitivity_decrease_button.pack(in_=self.sensitivity_setting, side=tk.LEFT, fill=None, padx=10)
        self.sensitivity_level_label.pack(in_=self.sensitivity_setting, side=tk.LEFT, fill=tk.BOTH, padx=30)
        self.sensitivity_increase_button.pack(in_=self.sensitivity_setting, side=tk.RIGHT, fill=None, padx=10)
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

        ## remove elements
        element_list = [\
            self.status_bar,
            self.camera_status_label,
            self.robot_status_label,
            self.imu1_status_label,
            self.imu2_status_label,
            self.settings_button,
            self.start_button,
            self.language_button,
            self.records_button,
            self.prev_session_info_1,
            self.prev_session_info_2,
            self.session_history,
            self.records_session_history_label,
            self.separator,
            self.records_previous_session_label,
            self.records_previous_session_datetime,
            self.records_previous_session_duration_label,
            self.records_previous_session_duration,
            self.records_previous_session_cadence_label,
            self.records_previous_session_cadence,
            self.records_previous_session_stride_time_label,
            self.records_previous_session_stride_time,
            self.records_table_wrapper,
            self.records_table,
            self.delete_records_button,
            self.volume_button,
            self.sensitivity_button,
            self.language_1_button,
            self.language_2_button,
            self.language_label,
            self.metronome_button,
            self.metronome_play_button,
            self.metronome_slider,
            self.volume_image_button,
            self.volume_slider,
            self.sensitivity_setting,
            self.sensitivity_level_label,
            self.sensitivity_desc_label,
            self.sensitivity_decrease_button,
            self.sensitivity_increase_button,
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
        
        global t, s, camera
        start_stop_flag = global_params.startFlag
        
        #### Session Started
        if global_params.startFlag == 0:
            global_params.startFlag = 1
            
            ## disable buttons when session is ongoing; unable to press
            self.settings_button.configure(state='disable')
            self.records_button.configure(state='disable')

            ## toggles start/stop button
            self.start_button.configure(image=self.start_button_red_photo, text=global_params.gui_lang["stop"])

            ## starts camera tracking and robot on separate thread
            global_params.stop_trackerFollower = False
            t = threading.Thread(target=global_params.trackerFollower, \
                                 args=(global_params.camera, global_params.camera_resolution, \
                                       global_params.robot, \
                                       global_params.cue, global_params.encouragement, \
                                       global_params.stop_trackerFollower, \
                                       global_params.sensitivity_level,) \
                                )
            t.start()

            ## starts output recording on separate thread
            global_params.stop_recordStream = False
            s = threading.Thread(target=global_params.recordStream)
            s.start()

            ## track session start time
            self.prev_session_start_time = datetime.now()
            

        #### Session Stopped
        else:
            global_params.startFlag = 0
            
            ## enable buttons; able to press
            self.settings_button.configure(state='normal')
            self.records_button.configure(state='normal')

            ## toggles start/stop button
            self.start_button.configure(image=self.start_button_green_photo, text=global_params.gui_lang["start"])
            
            ## stops camera tracking and robot, closes thread
            global_params.stop_trackerFollower = True
            t.join()

            ## stops output recording, closes thread
            global_params.stop_recordStream = True
            f = open('datafile.csv', 'a')
            f.close()
            s.join()

            ## track session stop time
            self.prev_session_stop_time = datetime.now()

            ## update records
            self.datetime_val = self.prev_session_start_time.strftime("%d/%m/%Y  %I:%M %p")
            self.datetime_txt.set(self.datetime_val)
            
            self.duration_in_s = (self.prev_session_stop_time - self.prev_session_start_time).total_seconds()
            self.duration_val = str(divmod(self.duration_in_s, 60)[0])
            self.duration_txt.set(self.duration_val + ' ' + global_params.gui_lang['duration_units'])

            self.cadence_val, self.stride_time_val = getCadenceStrideTime()
            self.cadence_txt.set(str(self.cadence_val) + ' ' + global_params.gui_lang['cadence_units'])
            self.stride_time_txt.set(str(self.stride_time_val) + ' ' + global_params.gui_lang['stride_time_units'])

            ## add record to table
            for i in range(0,8):
                if self.records_list[i][1] == '-':
                    self.records_list.remove(self.records_list[i])
                    break
                else:
                    if i == 7:
                        self.records_list.remove(self.records_list[-1])
            record = (str(i+1), self.datetime_val, self.duration_val, str(self.cadence_val), str(self.stride_time_val))
            self.records_list.append(record)
            
            self.records_list = sorted(self.records_list, reverse=True, key=lambda x: convertToUnixTime(x[1]))

            for i in range(0, len(self.records_list)):
                self.records_list[i] = list(self.records_list[i])
                self.records_list[i][0] = i+1
                self.records_list[i] = tuple(self.records_list[i])

            ## refresh records table
            self.RefreshRecords(self.records_list)

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
        elif lang == 1:
            global_params.cue = glob.glob('rsc/audio/cn_cue-*.wav')
            global_params.encouragement = glob.glob('rsc/audio/cn_encouragement-*.wav')
            
            global_params.language = '中文'
            global_params.gui_lang = {
                "settings" : "设置",
                "language" : "语言",
                "records" : "记录",
                "volume" : "音量",
                "metronome" : "节拍器",
                "back" : "返回",
                "start" : "开始",
                "stop" : "停止",
                "previous_session" : "上一次的理疗",
                "session_history" : "理疗记录",
                "delete" : "删除",
                "session_date" : "理疗日期\n(日/月/年)",
                "duration": "时长",
                "duration_units": "分钟",
                "cadence": "步频",
                "cadence_units": "步数/分钟",
                "stride_time": "步幅\n时间",
                "stride_time_units": "秒钟",
                "sensitivity": "速度",
                "sensitivity_desc": "调整机器人速度",
            }

        ## changes gui elements to display in selected language
        self.settings_button.configure(text=global_params.gui_lang["settings"])
        self.records_button.configure(text=global_params.gui_lang["records"])
        self.language_button.configure(text=global_params.gui_lang["language"])
        self.volume_button.configure(text=global_params.gui_lang["volume"])
        self.start_button.configure(text=global_params.gui_lang["start"])
        self.metronome_button.configure(text=global_params.gui_lang["metronome"])
        self.return_button.configure(text=global_params.gui_lang["back"])
        self.return_settings_button.configure(text=global_params.gui_lang["back"])

        self.previous_session_label_txt.set(global_params.gui_lang["previous_session"])
        self.session_history_label_txt.set(global_params.gui_lang["session_history"])
        self.delete_records_button.configure(text=global_params.gui_lang["delete"])
        self.duration_label_txt.set(global_params.gui_lang["duration"])
        self.cadence_label_txt.set(global_params.gui_lang["cadence"])
        self.stride_time_label_txt.set(global_params.gui_lang["stride_time"].replace('\n',' '))
        self.duration_txt.set(self.duration_val + ' ' + global_params.gui_lang['duration_units'])
        self.cadence_txt.set(self.cadence_val + ' ' + global_params.gui_lang['cadence_units'])
        self.stride_time_txt.set(self.stride_time_val + ' ' + global_params.gui_lang['stride_time_units'])
        self.records_table.heading("session_datetime",text=global_params.gui_lang["session_date"]+"\n")
        self.records_table.heading("session_duration",text=global_params.gui_lang["duration"]+"\n("+global_params.gui_lang["duration_units"]+")")
        self.records_table.heading("cadence",text=global_params.gui_lang["cadence"]+"\n("+global_params.gui_lang["cadence_units"]+")")
        self.records_table.heading("stride_time",text=global_params.gui_lang["stride_time"]+" ("+global_params.gui_lang["stride_time_units"]+")")
        
        self.lang_select_val.set('Language Selected: ' + global_params.language)

        self.sensitivity_level_val.set(global_params.gui_lang['sensitivity'])
        self.sensitivity_desc_val.set(global_params.gui_lang['sensitivity_desc'])

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

    def IncreaseSensitivity(self):
        ''' INCREASE SENSITIVITY
        Args:
            sensitivity_level      : (int, required)  Given sensitivity level integer.
        
        Returns:
            
        '''
        
        MAX_SENSITIVITY_LEVEL = 7
        if global_params.sensitivity_level == MAX_SENSITIVITY_LEVEL:
            global_params.sensitivity_level = MAX_SENSITIVITY_LEVEL
        else:
            global_params.sensitivity_level += 1
        
        self.sensitivity_level_val.set(str(global_params.sensitivity_level+1))
        return global_params.sensitivity_level
    
    def DecreaseSensitivity(self):
        ''' DECREASE SENSITIVITY
        Args:
            sensitivity_level      : (int, required)  Given sensitivity level integer.
        
        Returns:
            
        '''
        
        MIN_SENSITIVITY_LEVEL = 0
        if global_params.sensitivity_level == MIN_SENSITIVITY_LEVEL:
            global_params.sensitivity_level = MIN_SENSITIVITY_LEVEL
        else:
            global_params.sensitivity_level -= 1
        
        self.sensitivity_level_val.set(str(global_params.sensitivity_level+1))
        return global_params.sensitivity_level