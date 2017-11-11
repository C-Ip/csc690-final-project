#!/usr/bin/python3

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class Model(QWidget):
    W = 0
    H = 0
    B = 0
    timelineCount = 0
    importLabel = []
    videoList = []
    fname = None
    buttonList = []
