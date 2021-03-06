import sys
import os
import subprocess
from fbs_runtime.platform import *
from fbs_runtime.application_context import cached_property, \
    is_frozen
from fbs_runtime.application_context.PyQt5 import ApplicationContext, \
    cached_property
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# from PyQt5.QtSql import *
# from PyQt5.QtWebEngineWidgets import *
# from PyQt5.QtWebEngineCore import *

# import our local settings from settings.py
from qvpnstatus.settings import *

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
# https://leomoon.com/journal/python/high-dpi-scaling-in-pyqt5/
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

if is_mac():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontUseNativeMenuBar,
                                        True)  # use non native Menu bar so all options work.


class AppContext(ApplicationContext):
    def run(self):
        version = self.build_settings['version']
        QApplication.setApplicationName("QVpnStatus")
        QApplication.setOrganizationName("qvpnstatus")
        QApplication.setOrganizationDomain("example.com")
        QApplication.setApplicationVersion(self.build_settings['version'])
        QCoreApplication.setApplicationVersion(self.build_settings['version'])
        # Then we create a QSettings for our tool. Qt stores this using your company name and your application name
        # This setting is then saved in the correct place for your user and their operating system
        # Qt takes care of that for you, so you don't need to worry about handling it on different operating systems etc..
        # Your company name can be just your name but should remain consistent between your tools.
        # Your tool name should however be unique to each tool or application you create.
        self.settings = QSettings()
        # Uncommment the below line to see settings filename and path printed
        # print(self.settings.fileName())
        current_version = version
        self.settings.setValue('version', str(current_version))
        self.appctx = appctxt
        self.app_icon_path = self.appctx.get_resource('images')
        self.qIcon = lambda name: QtGui.QIcon(os.path.join(self.app_icon_path, name))

        # Splash startup screen initialization
        self.splash = QSplashScreen(
            QPixmap(os.path.join(self.app_icon_path, 'logo.png')))
        self.splash.show()

        # self.main_window.setWindowTitle("App Name v" + version)
        self.main_window.setWindowTitle(f"{QApplication.applicationName()} v{QApplication.applicationVersion()}")

        self.main_window.show()
        self.splash.finish(self.main_window)
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MainWindow(self)


class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        mainwindow_ui = appctxt.get_resource("ui/mainwindow.ui")
        uic.loadUi(mainwindow_ui, self)
        self.ctx = ctx
        self.appctx = appctxt
        self.settings = self.ctx.settings
        # Setup appctx override for inside mainwindow to utilize fbs: https://build-system.fman.io/manual/#get_resource
        self.app_icon_path = self.appctx.get_resource('images')
        qIcon = lambda name: QtGui.QIcon(os.path.join(self.app_icon_path, name))
        # self.setupUi(self)
        # Initialize status bar
        self.status_bar = self.statusBar()

        # Then we look at our settings to see if there is a setting called geometry saved. Otherwise we default to an empty string
        # geometry = self.settings.value('geometry', bytes('', 'utf-8'))

        # Then we call a Qt built in function called restoreGeometry that will restore whatever values we give it.
        # In this case we give it the values from the settings file.
        try:
            if self.settings.contains("geometry"):
                try:
                    geometry = self.settings.value('geometry', bytes('', 'utf-8'))
                    self.restoreGeometry(geometry)
                except:
                    pass
            else:
                print('Unable to restore geometry')
                pass
        except:
            pass

        # Setup keybindings for Edit
        self.actionCut.setShortcuts(QKeySequence.Cut)
        self.actionCopy.setShortcuts(QKeySequence.Copy)
        self.actionPaste.setShortcuts(QKeySequence.Paste)

        self.actionCut.setIcon(qIcon('edit-cut.png'))
        self.actionCopy.setIcon(qIcon('edit-copy.png'))
        self.actionPaste.setIcon(qIcon('edit-paste.png'))
        self.actionQuit.setIcon(qIcon('exit.png'))

        # Put all your custom signals slots and other code below here.
        self.actionAbout.triggered.connect(self.about_dialog)

    # Put all your custom functions here

    def about_dialog(self):
        self.show_status_bar_message('Activated About Qaction', 10000)

    @QtCore.pyqtSlot()
    def show_status_bar_message(self, message, timeout=5000):
        self.status_bar.showMessage(str(message), timeout)
        pass

    def closeEvent(self, event):
        # Now we define the closeEvent This is called whenever a window is closed. It is passed an event which we can
        # choose to accept or reject, but in this case we'll just pass it on after we're done.

        # First we need to get the current size and position of the window.
        # This can be fetched using the built in saveGeometry() method.
        # This is got back as a byte array. It won't really make sense to a human directly, but it makes sense to Qt.
        geometry = self.saveGeometry()

        # Once we know the geometry we can save it in our settings under geometry
        self.settings.setValue('geometry', geometry)

        # Finally we pass the event to the class we inherit from. It can choose to accept or reject the event,
        # but we don't need to deal with it ourselves
        super(MainWindow, self).closeEvent(event)

        # Save settings: Define any other settings that should be saved on close.
        # self.settings.setValue('setting_name', str(somevalue))


import sys

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
