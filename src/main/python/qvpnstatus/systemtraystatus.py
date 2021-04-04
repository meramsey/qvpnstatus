import os
import sys
from fbs_runtime.platform import *
from fbs_runtime.application_context import cached_property, \
    is_frozen
from fbs_runtime.application_context.PyQt5 import ApplicationContext, \
    cached_property
import psutil
import functools
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtMultimedia
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QActionGroup
from PyQt5.QtMultimedia import QSound
import nmcli
from qvpnstatus.settings import *

# Disable Sudo for nmcli so it runs as the user with access to all the configs details
# https://itectec.com/ubuntu/ubuntu-connect-disconnect-from-vpn-from-the-command-line/ Also note that regular users
# usually don't have permission to control networking. Using the commands above with sudo should work for most
# connections, but VPN specifically might fail with "Error: Connection activation failed: no valid VPN secrets."
nmcli.disable_use_sudo()


app = QApplication([])
app.setQuitOnLastWindowClosed(False)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, monitoring_mode=False):
        self.appctx = appctxt
        QtWidgets.QSystemTrayIcon.__init__(self)
        QApplication.setApplicationName("QVpnStatus")
        QApplication.setOrganizationName("qvpnstatus")
        QApplication.setOrganizationDomain("wizardassistant.com")
        self.settings = app_settings
        self.setIcon(QIcon(icon))
        self.menu = QtWidgets.QMenu()
        self.vpnmenu = self.menu.addMenu('VPN Connections')
        self.preferences_menu = self.menu.addMenu('Settings')
        self.sounds_enabled_action = self.preferences_menu.addAction('Sound Notifications')
        self.sounds_enabled_action.setCheckable(True)
        self.sounds_enabled_action.setChecked(True)
        self.intervalmenu = self.preferences_menu.addMenu('Check Interval')
        self.menu_interval_group = QActionGroup(self)
        self.create_intervals_menuactions()
        self.menu_interval_group.isExclusive()

        # Monitoring MODE
        self.menu_monitoring_action = self.menu.addAction("Monitoring mode")
        self.menu_monitoring_action.setCheckable(True)
        self.menu_monitoring_action.setChecked(False)
        self.menu_monitoring_action.setStatusTip('Toggle VPN Monitoring Mode for network manager Connections.')
        self.default_interval = int(default_interval)
        self.monitor = monitor_mode
        self.sounds = sound_notifications
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(self.default_interval)  # in milliseconds, so 5000 = 5 seconds
        # self.timer.timeout.connect(self.check_vpn_status)
        self.timer_nmcli = QTimer(self)
        self.timer_nmcli.setSingleShot(False)
        self.timer_nmcli.setInterval(self.default_interval)  # in milliseconds, so 5000 = 5 seconds
        self.timer_nmcli.timeout.connect(self.check_vpns_status_nmcli)
        self.get_vpn_connections_linux()
        self.timer.start()
        self.timer_nmcli.start()

        self.sounds_enabled_action.triggered.connect(self.sounds_enabled)
        self.menu_monitoring_action.toggled.connect(self.monitoring_mode)

        self.menu.addSeparator()
        # EXIT
        exit_action = self.menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_zero)

        self.setContextMenu(self.menu)
        self.restore_settings()

    @staticmethod
    def value_to_bool(value):
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    def sounds_enabled(self, checked):
        print(f'Sounds Enabled triggered with {checked}')
        self.sounds = self.value_to_bool(checked)
        self.show_message('QVPN Status', f'Sound Notifications set to {self.sounds}.', qIcon('active_shield.png'))
        if self.sounds:
            self.sound_notify(qSound("538149__fupicat__notification.wav"))
        self.settings.setValue('sound_notifications', self.sounds)

    def create_intervals_menuactions(self):
        for interval in intervals:
            self.intervalmenu.addAction(str(f'{interval} Secs'), functools.partial(self.set_interval, interval))
        for action in self.intervalmenu.actions():
            action.setCheckable(True)
            self.menu_interval_group.addAction(action)
            if action.text() == '10 Secs':
                action.setChecked(True)

    def set_interval(self, interval):
        self.default_interval = int(interval * 1000)
        self.timer.start(self.default_interval)
        self.timer_nmcli.start(self.default_interval)
        print(f'Check Interval Changed to {interval}')
        self.settings.setValue('default_interval', int(self.default_interval))

    def set_icon(self, icon):
        self.setIcon(icon)

    def show_message(self, title, msg, icon):
        self.showMessage(title, msg, icon)

    def sound_notify(self, sound):
        if self.sounds:
            return sound

    def monitoring_mode(self, checked):
        if self.menu_monitoring_action.isChecked():
            self.sound_notify(qSound("538149__fupicat__notification.wav"))
            self.show_message('QVPN Status', 'Monitoring Mode ENGAGED.', qIcon('active_shield.png'))
            self.monitor = True
            self.check_vpns_status_nmcli()
        else:
            self.sound_notify(qSound("538149__fupicat__notification.wav"))
            self.show_message('QVPN Status', 'Monitoring Mode DISABLED!', QIcon(qIcon('inactive_shield.png')))
            self.monitor = False
        self.settings.setValue('monitor_mode', self.menu_monitoring_action.isChecked())

    def get_vpn_connections_linux(self):
        for conn in nmcli.connection():
            if conn.conn_type == 'vpn':
                # print(conn)
                name = str(conn.name)
                self.vpnmenu.addAction(name, functools.partial(self.printMe, name))
        for action in self.vpnmenu.actions():
            action.setCheckable(True)

    def printMe(self, text):
        print(f"{text} selected")

    def check_vpns_status_nmcli(self):
        print('VPN checks engaged')
        if self.menu_monitoring_action.isChecked():
            for action in self.vpnmenu.actions():
                # print(action.text())
                if action.isChecked():
                    try:
                        connection = action.text()
                        if nmcli.connection.show(connection)['GENERAL.STATE'] == 'activated':
                            print(f'VPN {connection} Up')
                            self.set_icon(qIcon('active_shield.png'))
                    except KeyError:
                        self.set_icon(qIcon('inactive_shield.png'))
                        self.sound_notify(qSound("514152__edwardszakal__alert.wav"))
                        self.showMessage('VPN Status',
                                         f'VPN {action.text()} down Trying to Reconnect. Please check '
                                         f'and accept any 2FA Pushes', QSystemTrayIcon.Critical)
                        try:
                            nmcli.connection.up(action.text())
                        except:
                            self.sound_notify(qSound("514152__edwardszakal__alert.wav"))
                            self.showMessage('VPN Status', f'VPN {action.text()} still down..',
                                             QSystemTrayIcon.Critical)
                            self.set_icon(qIcon('inactive_shield.png'))
                            print(f'VPN {action.text()} down')
                            pass

    def check_vpn_status_adapter(self):
        """Psutils method based on tun/tap adapter. Probably will remove unless ends up being useful on Windows"""
        if self.menu_monitoring_action.isChecked():
            try:
                print(psutil.net_if_stats()[tun])
                nic_status, nic_duplex, nic_speed, nic_mtu = psutil.net_if_stats()[tun]
                family, address, netmask, broadcast, ptp = psutil.net_if_addrs()[tun][0]
                if nic_status:
                    print(f'VPN {tun} Up')
                    self.set_icon(qIcon('active_shield.png'))
            except KeyError:
                qSound("514152__edwardszakal__alert.wav")
                self.showMessage('VPN Status', f'VPN {tun} down. Trying to Reconnect. Please check and accept any 2FA '
                                               f'Pushes', QSystemTrayIcon.Critical)
                self.set_icon(qIcon('inactive_shield.png'))
                print(f'VPN {tun} down')
                pass

    def restore_settings(self):
        # Restore  VPN checked state settings
        for action in self.vpnmenu.actions():
            action.setChecked(self.value_to_bool(app_settings.value(action.text())))
        self.menu_monitoring_action.setChecked(self.value_to_bool(app_settings.value('monitor_mode')))
        self.sounds_enabled_action.setChecked(self.value_to_bool(app_settings.value('sound_notifications')))

    def save_settings(self):
        # Save settings
        for action in self.vpnmenu.actions():
            self.settings.setValue(str(action.text()), action.isChecked())
        self.settings.setValue('monitor_mode', self.menu_monitoring_action.isChecked())
        self.settings.setValue('default_interval', int(self.default_interval))
        self.settings.setValue('sound_notifications', self.sounds)
        self.settings.sync()

    def exit_zero(self, checked):
        self.save_settings()
        sys.exit(0)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    tray = SystemTrayIcon(qIcon('inactive_shield.png'))
    tray.setVisible(True)
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
