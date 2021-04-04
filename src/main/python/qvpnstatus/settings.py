import os
import sys
from PyQt5.QtMultimedia import QSound
from fbs_runtime.platform import is_mac, is_linux, is_windows
from pathlib import Path
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Get absolute path to current dir app is running from even when frozen
app_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])))

# Create app icons path from above and setup lambda to make it easy to use
app_icon_path = os.path.join(app_path, 'images')
qIcon = lambda name: QtGui.QIcon(os.path.join(app_icon_path, name))

# Create app icons path from above and setup lambda to make it easy to use
sounds_icon_path = os.path.join(app_path, 'sounds')

# Sounds lambda
qSound = lambda name: QSound.play(os.path.join(sounds_icon_path, name))

# Create ui files path from app path and setup lambda to make it easy to use
ui_dir = os.path.join(app_path, 'ui')
ui_path = lambda name: (os.path.join(ui_dir, name))
ui_loader = lambda name, parent: uic.loadUi(ui_path(name), parent)

# Setup Qsettings for app name
app_settings = QtCore.QSettings('qvpnstatus', 'QVpnStatus')
config_data_dir = Path("qvpnstatus/QVpnStatus")

# Define and setup and ensure app config path is writable
app_config_data_dir = QStandardPaths.writableLocation(
    QStandardPaths.AppConfigLocation) / config_data_dir

os.makedirs(app_config_data_dir, exist_ok=True)

# Lambda for referencing files in this path
DataDirPath = lambda name: app_config_data_dir / name

# Setup settings restoration

# Example
if app_settings.contains("sound_notifications"):
    # there is the key in QSettings
    print('Checking for sound notification preference in config')
    sound_notifications = app_settings.value('sound_notifications')
    print(f"Found sound_notifications in config: {sound_notifications}")
else:
    print('sound_notifications not found in config. Using default Enabled')
    app_settings.setValue('sound_notifications', True)
    sound_notifications = app_settings.value('sound_notifications')
    pass


if app_settings.contains("default_interval"):
    # there is the key in QSettings
    print('Checking for default_interval preference in config')
    default_interval = app_settings.value('default_interval')
    print(f"Found default_interval in config: {default_interval}")
else:
    print('default_interval not found in config. Using default 10 secs')
    app_settings.setValue('default_interval', 10000)
    default_interval = int(app_settings.value('default_interval'))
    pass

if app_settings.contains("monitor_mode"):
    # there is the key in QSettings
    print('Checking for monitor_mode preference in config')
    monitor_mode = app_settings.value('monitor_mode')
    print(f"Found monitor_mode in config: {monitor_mode}")
else:
    print('monitor_mode not found in config. Using default 10 secs')
    app_settings.setValue('monitor_mode', False)
    monitor_mode = app_settings.value('monitor_mode')
    pass

# Define global variables
tun = ''
intervals = [5, 10, 15, 30, 60, 120, 180, 300]
