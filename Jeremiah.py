# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:31:46 2019

"""

import sys
from PyQt5.QtCore import QSettings, QResource, QCoreApplication
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine

from connectors import Connector

QCoreApplication.setOrganizationName("Deuteronomy Works")
QCoreApplication.setApplicationName("Jeremiah")
settings = QSettings()

# QResource.registerResource("resource.rcc")

app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon("icons/logo.png"))

connector = Connector()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("Connector", connector)
engine.load("main.qml")
engine.quit.connect(app.quit)

sys.exit(app.exec_())
