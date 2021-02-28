from clear_cache import clear as clear_cache
from sys import exit as return_exit
from os import getlogin as get_user_name
from os import access as file_exists
from os import F_OK as file_exists_param
from os.path import join as join_path
from os.path import isdir as is_folder
from PyQt5 import QtWidgets as Widgets
from PyQt5.QtGui import QPixmap as NewPixmap
from ui import Ui_MainWindow as NewMainWindow
from threading import Thread as NewThread
from win32api import GetSystemMetrics as GetScreenSize
from pyautogui import screenshot as shot
from pyautogui import position as pos
from numpy import array as np_array
from PIL import ImageDraw
import cv2


height = int(GetScreenSize(0))
width = int(GetScreenSize(1))


is_recording = False
is_paused = False


show_cursor = True
mouse_script = 'rectangle(((mouse_x, mouse_y), (mouse_x + 10, mouse_y + 10)), width=1, outline=0, fill=((255, 255, ' \
               '255))) '
video_filename = 'Recording'
video_format = 'mp4'
video_path = f'C:\\Users\\{get_user_name()}\\Screen Reader\\'


def get_video_path():
    full_path = join_path(video_path, video_filename)
    if file_exists(f'{full_path}.{video_format}', file_exists_param):
        i = 1
        while True:
            if file_exists(f'{full_path} ({i}).{video_format}', file_exists_param):
                i += 1
            else:
                return f'{full_path} ({i}).{video_format}'
    else:
        return f'{full_path}.{video_format}'


def select_video_path():
    dialog = Widgets.QFileDialog()
    foo_dir = dialog.getExistingDirectory(MainWindow, 'Select Path')
    ui.videopathEdit.setText(foo_dir.replace('/', '\\'))


def setup_ui():
    ui.recordButton.mousePressEvent = toggle_record
    ui.pauseButton.mousePressEvent = toggle_pause
    ui.videopathButton.clicked.connect(select_video_path)
    ui.videopathEdit.setText(video_path)


def recorder():
    global is_recording
    global is_paused
    resolution = (width, height)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = get_video_path()
    out = cv2.VideoWriter(filename, codec, 20, resolution)
    while is_recording:
        while not is_paused:
            img = shot()
            if show_cursor:
                draw = ImageDraw.Draw(img)
                mouse_x, mouse_y = pos()
                for i in mouse_script.split('\n'):
                    if i:
                        eval(f'draw.{i}')
            frame = cv2.cvtColor(np_array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)
    is_recording = False
    is_paused = False
    out.release()


def toggle_pause(e):
    global is_paused
    if is_paused:
        is_paused = False
        ui.pauseButton.setPixmap(NewPixmap('pause.png'))
    else:
        is_paused = True
        ui.pauseButton.setPixmap(NewPixmap('record.png'))


def toggle_record(e):
    global is_recording
    global is_paused
    global video_format
    global video_path
    if is_recording:
        is_paused = True
        is_recording = False
        ui.pauseButton.setDisabled(True)
        ui.recordButton.setPixmap(NewPixmap('record.png'))
        ui.pauseButton.setPixmap(NewPixmap('pause.png'))
    else:
        is_paused = False
        is_recording = True
        ui.recordButton.setPixmap(NewPixmap('stop.png'))
        video_format = ui.videoformatEdit.text()
        video_path = ui.videopathEdit.text()
        NewThread(target=recorder).start()
        ui.pauseButton.setEnabled(True)


app = Widgets.QApplication([__name__])
MainWindow = Widgets.QMainWindow()
ui = NewMainWindow()
ui.setupUi(MainWindow)
setup_ui()
MainWindow.show()
result = app.exec_()
clear_cache()
return_exit(result)
