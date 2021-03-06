from clear_cache import clear as clear_cache
from sys import exit as return_exit
from os import access as file_exists
from os import F_OK as file_exists_param
from os import mkdir as make_dir
from os import name as os_type
from os import getcwd as get_current_dir
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


is_recording = False
is_paused = False
screen_width = int(GetScreenSize(0))
screen_height = int(GetScreenSize(1))


mouse_script = 'draw.rectangle(((mouse_x - 5, mouse_y - 5), (mouse_x + 5, mouse_y + 5))'
mouse_script += ', width=1, outline=0, fill=((255, 255, 255)))'
video_filename = 'Recording'
video_format = 'mp4'
video_path = get_current_dir()
if os_type == 'nt':
    from os import getlogin as get_user_name
    video_path = f'C:\\Users\\{get_user_name()}\\Videos\\Screen Reader\\'


def get_video_path():
    if not is_folder(video_path):
        make_dir(video_path)
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


def stop_record():
    global is_recording
    global is_paused
    is_paused = True
    is_recording = False


def select_video_path():
    dialog = Widgets.QFileDialog()
    foo_dir = dialog.getExistingDirectory(MainWindow, 'Select Path')
    ui.videopathEdit.setText(foo_dir.replace('/', '\\'))


def load_config():
    global mouse_script
    global video_filename
    global video_format
    global video_path
    if file_exists('config.txt', file_exists_param):
        temp_f = open('config.txt', 'r')
        config = temp_f.read().split('\n')
        temp_f.close()
        video_path = config[0]
        video_filename = config[1]
        video_format = config[2]
        ui.xEdit.setText(config[3])
        ui.yEdit.setText(config[4])
        ui.widthEdit.setText(config[5])
        ui.heightEdit.setText(config[6])
    if file_exists('mouse_script.txt', file_exists_param):
        temp_f = open('mouse_script.txt', 'r')
        mouse_script = temp_f.read()
        temp_f.close()
        ui.mousescriptText.setPlainText(mouse_script)


def save_config():
    temp_f = open('config.txt', 'w')
    config = f'{video_path}\n{video_filename}\n{video_format}\n{ui.xEdit.text()}\n{ui.yEdit.text()}\n'
    config += f'{ui.widthEdit.text()}\n{ui.heightEdit.text()}'
    temp_f.write(config)
    temp_f.close()
    temp_f = open('mouse_script.txt', 'w')
    temp_f.write(
        mouse_script
    )
    temp_f.close()


def setup_ui():
    load_config()
    ui.recordButton.mousePressEvent = toggle_record
    ui.pauseButton.mousePressEvent = toggle_pause
    ui.videopathButton.clicked.connect(select_video_path)
    ui.videopathEdit.setText(video_path)
    ui.videofilenameEdit.setText(video_filename)
    ui.videoformatEdit.setText(video_format)


def recorder():
    global is_recording
    global is_paused
    global mouse_script
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = get_video_path()
    mouse_script = ui.mousescriptText.toPlainText()
    left, top, width, height = 0, 0, screen_width, screen_height
    try:
        left = int(ui.xEdit.text())
        top = int(ui.yEdit.text())
        width = int(ui.widthEdit.text())
        height = int(ui.heightEdit.text())
    except ValueError:
        is_paused = True
        is_recording = False
        ui.pauseButton.setDisabled(True)
        ui.recordButton.setPixmap(NewPixmap('record.png'))
        ui.pauseButton.setPixmap(NewPixmap('pause.png'))
    if left < 0:
        left = 0
    if top < 0:
        top = 0
    if left > screen_width:
        left = 0
    if top > screen_height:
        top = 0
    if width + left > screen_width:
        width = screen_width - left - 1
    if height + top > screen_height:
        height = screen_height - height - 1
    out = cv2.VideoWriter(filename, codec, 20, tuple((width, height)))
    while is_recording:
        while not is_paused:
            img = shot().crop((left, top, width + left, height + top))
            draw = ImageDraw.Draw(img)
            mouse_x, mouse_y = pos()
            if mouse_script:
                for i in mouse_script.split('\n'):
                    if i:
                        eval(i)
            frame = cv2.cvtColor(np_array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)
    out.release()
    cv2.destroyAllWindows()
    is_recording = False
    is_paused = False


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
    global video_filename
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
        video_filename = ui.videofilenameEdit.text()
        NewThread(target=recorder).start()
        ui.pauseButton.setEnabled(True)


app = Widgets.QApplication([__name__])
MainWindow = Widgets.QMainWindow()
ui = NewMainWindow()
ui.setupUi(MainWindow)
setup_ui()
MainWindow.show()
result = app.exec_()
save_config()
stop_record()
clear_cache()
return_exit(result)
