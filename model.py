#!/usr/bin/python3

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class Model(QWidget):
    W = 0
    H = 0
    B = 0
    pausedTime = 0
    timelineCount = 0
    importLabel = []
    videoList = []
    fname = None
    aname = None
    buttonList = []
    importList = []
    videoListLength = [0]*20
    current = 0
    adioCurrent = 0
    currentTimeVid = 1
    subtitleList = []
    subList = []
    subtitleButtonList = []
    positionarray = []
    importAudioList = []
    audioList = []
    audioThumbList = []
    importBoxState = 3
    currentVidTimeLineIndex = 0
    currentAudioTimeIndex = 0
    timelineState = False
    videos = []
    tempIndex = 0
    od = []
    durationlist = []
    videoDuration = 0
    additionalduration = 0
    temp = 0
