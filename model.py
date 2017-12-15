#!/usr/bin/python3

'''

Fall 2017 CSC 690

File: videoEditor.py

By: Calvin Ip & Jerry AuYeung
Last revised: 12/14/2017

Model for videoEditor.py. This file only holds the variables we used.

'''

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class Model(QWidget):
    W = 0
    H = 0
    B = 0
    pausedTime = 0
    pausedAudio = 0
    audioTime = 0
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
    audiotempIndex = 0
    anothertempduration =0
    temptime = 0

    delayTimes=[]
    delayCount = 0
    i =0

    subtitleStart = []
    subtitleDuration = []
    subtitleIndex = 0
    subTimePause = 0
    soundPosition = 0


