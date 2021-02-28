from clear_cache import clear as clear_cache
from sys import exit as return_exit
from PyQt5 import QtWidgets as Widgets
from PyQt5.QtGui import QPixmap as NewPixmap
from ui import Ui_MainWindow as NewMainWindow
from threading import Thread as NewThread
from win32api import GetSystemMetrics as GetScreenSize
from pyautogui import screenshot as shot
from numpy import array as np_array
import cv2


height = int(GetScreenSize(0))
width = int(GetScreenSize(1))


is_recording = False
is_paused = False


def setup_binds():
    ui.recordButton.mousePressEvent = toggle_record
    ui.pauseButton.mousePressEvent = toggle_pause


def recorder():
    global is_recording
    global is_paused
    resolution = (1280, 1024)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = "Recording.mp4"
    out = cv2.VideoWriter(filename, codec, 20, resolution)
    while is_recording:
        while not is_paused:
            img = shot()
            frame = cv2.cvtColor(np_array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)
    is_recording = False
    is_paused = False
    out.release()


def toggle_pause(e):
    global is_paused
    is_paused = not is_paused


def toggle_record(e):
    global is_recording
    global is_paused
    if is_recording:
        is_paused = True
        is_recording = False
        ui.pauseButton.setDisabled(True)
        ui.recordButton.setPixmap(NewPixmap('record.png'))
    else:
        is_paused = False
        is_recording = True
        ui.recordButton.setPixmap(NewPixmap('stop.png'))
        NewThread(target=recorder).start()
        ui.pauseButton.setEnabled(True)


app = Widgets.QApplication([__name__])
MainWindow = Widgets.QMainWindow()
ui = NewMainWindow()
ui.setupUi(MainWindow)
setup_binds()
MainWindow.show()
result = app.exec_()
clear_cache()
return_exit(result)
