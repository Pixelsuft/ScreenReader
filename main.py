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


def setup_binds():
    ui.recordButton.mousePressEvent = toggle_record


def recorder():
    resolution = (1280, 1024)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = "Recording.mp4"
    out = cv2.VideoWriter(filename, codec, 20, resolution)
    while is_recording:
        img = shot()
        frame = cv2.cvtColor(np_array(img), cv2.COLOR_BGR2RGB)
        out.write(frame)
    out.release()


def toggle_record(e):
    global is_recording
    if is_recording:
        is_recording = False
        ui.recordButton.setPixmap(NewPixmap('record.png'))
    else:
        is_recording = True
        ui.recordButton.setPixmap(NewPixmap('stop.png'))
        NewThread(target=recorder).start()


app = Widgets.QApplication([__name__])
MainWindow = Widgets.QMainWindow()
ui = NewMainWindow()
ui.setupUi(MainWindow)
setup_binds()
MainWindow.show()
result = app.exec_()
clear_cache()
return_exit(result)
