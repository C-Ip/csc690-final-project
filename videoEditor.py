#!/usr/bin/python3
import extendqlabel
import sys, os, cv2
from tkinter import filedialog
from tkinter import *
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from model import Model
import numpy as np

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Video Editor"
        
        
        self.display()
        self.initUI()
        self.toolbar()
        self.timeLine()
        self.createButtons()
        #self.createLabel()
        
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.move(500,20)
        self.videoWidget.resize(600,400)
        self.videoWidget.show()
        
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        
        self.show()
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 50, 1700, 850)

    def createLabel(self):
        Model.importLabel.append(QLabel(self))
        Model.importLabel[len(Model.videoList)-1].setGeometry(20+(150*(len(Model.videoList)-1)),560,150,130)
        Model.importLabel[len(Model.videoList)-1].setText(str(len(Model.videoList)))
        Model.importLabel[len(Model.videoList)-1].setStyleSheet("border: 2px solid black")
        Model.importLabel[len(Model.videoList)-1].setAlignment(Qt.AlignCenter)
        Model.importLabel[len(Model.videoList)-1].show()
    #QtCore.QObject.connect(Model.importLable[len(Model.videoList)-1],SIGNAL('clicked()'),lambda index:self.timelinetoVid(len(Model.videoList)-1,index))
    
    
    def display(self):
        self.displayLabel = QLabel(self)
        self.displayLabel.setStyleSheet("border: 2px solid black")
        self.displayLabel.setGeometry(500, 20, 600, 400)

    def toolbar(self):
        self.toolbarLabel = QLabel(self)
        self.toolbarLabel.setStyleSheet("border: 2px solid black")
        self.toolbarLabel.setGeometry(20, 450, 1400, 100)

    def timeLine(self):
        self.timeLineLabel = QLabel(self)
        self.timeLineLabel.setStyleSheet("border: 2px solid black")
        self.timeLineLabel.setGeometry(20, 560, 1400, 130)

        # Timeline for subtitles
        self.subTimeLineLabel = QLabel(self)
        self.subTimeLineLabel.setStyleSheet("border: 2px solid black")
        self.subTimeLineLabel.setGeometry(20, 700, 1400, 80)

    def createButtons(self):
        # Play button
        self.playButton = QPushButton("Play", self)
        self.playButton.setStyleSheet("background-color: gray")
        self.playButton.move(700, 500)
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.play)
        

        # Pause button
        self.pauseButton = QPushButton("Pause", self)
        self.pauseButton.setStyleSheet("background-color: gray")
        self.pauseButton.move(800, 500)
        self.pauseButton.clicked.connect(self.pause)
        

        # Import files button
        self.importButton = QPushButton("Import", self)
        self.importButton.setStyleSheet("background-color: gray")
        self.importButton.move(30, 460)
        self.importButton.clicked.connect(self.importFunction)

        # Change to fullscreen button
        self.fullScreenButton = QPushButton("Fullscreen", self)
        self.fullScreenButton.setStyleSheet("background-color: gray")
        self.fullScreenButton.move(1000, 380)

        # Turn on/off subtitle button
        self.subtitleButton = QPushButton("Subtitle ON/OFF", self)
        self.subtitleButton.setStyleSheet("background-color: gray")
        self.subtitleButton.move(900, 500)
    
    def mouseReleaseEvent(self,QMouseEvent):
        p = QMouseEvent.pos()
        if p.x() >20 and p.x()< 170 and p.y() > 560 and p.y() < 690:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[0])))
            self.playButton.setEnabled(True)
        if p.x() >20 + 150 and p.x()< 320 and p.y() > 560 and p.y() < 690:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[1])))
            self.playButton.setEnabled(True)
        self.videoWidget.show()
    
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def pause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def importFunction(self):
        Model.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '../desktop','All files(*.jpeg *.mp4);;Image files(*.jpeg);;Video Files(*.mp4)')
        if Model.fname != '':
            Model.videoList.append(Model.fname)
        print(str(len(Model.videoList)))
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.fname)))
        self.mediaPlayer.play()
        self.createLabel()
        self.update()

    def timelinetoVid(self):
        print("vid1")


    def timelinetoVid2(self):
        print("vid2")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browse = Window()
    sys.exit(app.exec_())
