from cx_Freeze import setup, Executable

setup(
    name='Screen Reader',
    version='1.1',
    description='Screen Recorder',
    executables = [Executable('main.py')]
)