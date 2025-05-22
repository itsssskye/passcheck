from setuptools import setup

APP = ['code.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'ttkbootstrap', 're'],
    'iconfile': 'icon.icns',
}

setup(
    app=APP,
    name='PassCheck',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)