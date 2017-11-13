#!/usr/bin/python3
import sys, os
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from model import Model
from functools import partial


class Window(QWidget):
    totalDuration = 0

    def __init__(self):
        super().__init__()
        self.title = "Video Editor"
        
        
        self.display()
        self.initUI()
        self.toolbar()
        self.timeLine()
        self.createButtons()
        self.importBox()
        #self.createLabel()
        
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setGeometry(700,20,600,400)
        

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        
        self.videoWidget.setAspectRatioMode(Qt.KeepAspectRatio)
        self.show()
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 50, 1700, 850)
    
    
    def createButton(self):
        Model.buttonList.append(QPushButton(str(len(Model.videoList)),self))
        Model.buttonList[len(Model.videoList)-1].move(20+(150*(len(Model.videoList)-1)),600)
        Model.buttonList[len(Model.videoList)-1].resize(150,130)
        Model.buttonList[len(Model.videoList)-1].setStyleSheet("border: 2px solid black")
        index = 0
        Model.buttonList[len(Model.videoList)-1].clicked.connect(partial(self.timelinetoVid, len(Model.videoList)-1))
        Model.buttonList[len(Model.videoList)-1].show()
    
    
    def importBox(self):
        self.importBoxLabel = QLabel(self)
        self.importBoxLabel.setStyleSheet("border: 2px solid black")
        self.importBoxLabel.setGeometry(20,20,600,400)
    
    """
    def createLabel(self):
        Model.importLabel.append(QLabel(self))
        Model.importLabel[len(Model.videoList)-1].setGeometry(20+(150*(len(Model.videoList)-1)),560,150,130)
        Model.importLabel[len(Model.videoList)-1].setText(str(len(Model.videoList)))
        Model.importLabel[len(Model.videoList)-1].setStyleSheet("border: 2px solid black")
        Model.importLabel[len(Model.videoList)-1].setAlignment(Qt.AlignCenter)
        Model.importLabel[len(Model.videoList)-1].show()
    #QtCore.QObject.connect(Model.importLable[len(Model.videoList)-1],SIGNAL('clicked()'),lambda index:self.timelinetoVid(len(Model.videoList)-1,index))
    """
    
    def display(self):
        self.displayLabel = QLabel(self)
        self.displayLabel.setStyleSheet("border: 2px solid black")
        self.displayLabel.setGeometry(700, 20, 600, 400)

    def toolbar(self):
        self.toolbarLabel = QLabel(self)
        self.toolbarLabel.setStyleSheet("border: 2px solid black")
        self.toolbarLabel.setGeometry(20, 450, 1400, 100)

    def timeLine(self):
        
        self.timeLineLabel = QLabel(self)
        self.timeLineLabel.setStyleSheet("border: 2px solid black")
        self.timeLineLabel.setGeometry(20, 600, 1400, 130)

        # Timeline for subtitles
        self.subTimeLineLabel = QLabel(self)
        self.subTimeLineLabel.setStyleSheet("border: 2px solid black")
        self.subTimeLineLabel.setGeometry(20, 740, 1400, 80)

    def durationChanged(self, duration):
        if Window.totalDuration == 0:
            self.playTimeLabel = QLabel(self)
        Window.totalDuration += duration
        print("Total duration: " + str(Window.totalDuration))
        self.seconds = int(round((duration/1000) % 60))
        self.minutes = int(round((duration/60000) % 60))
        self.hours = int(round((duration/3600000) % 24))
        print("Duration: " + str(duration))
        '''
        if self.hours < 10:
            self.playTimeLabel.setText("0" + str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds))
        if self.minutes < 10:
            self.playTimeLabel.setText(str(self.hours) + ":0" + str(self.minutes) + ":" + str(self.seconds))
        if self.seconds < 10:
            self.playTimeLabel.setText(str(self.hours) + ":" + str(self.minutes) + ":0" + str(self.seconds))
        else:
        '''
        self.playTimeLabel.setText(str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds))
        self.playTimeLabel.setStyleSheet("font-size: 40px")
        self.playTimeLabel.move(650, 550)
        self.playTimeLabel.show()
        

    def createButtons(self):
        # Play button
        self.playButton = QPushButton("Play", self)
        self.playButton.setStyleSheet("background-color: gray")
        self.playButton.move(700, 500)
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.play)
        

        # Import files button
        self.importButton = QPushButton("Import", self)
        self.importButton.setStyleSheet("background-color: gray")
        self.importButton.move(30, 460)
        self.importButton.clicked.connect(self.importFunction)

        # Change to fullscreen button
        self.fullScreenButton = QPushButton("Fullscreen", self)
        self.fullScreenButton.setStyleSheet("background-color: gray")
        self.fullScreenButton.move(1000, 380)

    """
    def mouseReleaseEvent(self,QMouseEvent):
        p = QMouseEvent.pos()
        if p.x() >20 and p.x()< 170 and p.y() > 560 and p.y() < 690:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[0])))
            self.playButton.setEnabled(True)
        if p.x() >20 + 150 and p.x()< 320 and p.y() > 560 and p.y() < 690:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[1])))
            self.playButton.setEnabled(True)
        self.videoWidget.show()
    """
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playButton.setText("Pause")

    def importFunction(self):
        Model.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '../desktop','All files(*.jpeg *.mp4 *.mov);;Image files(*.jpeg);;Video Files(*.mp4 *.mov)')
        if Model.fname != '':
            Model.videoList.append(Model.fname)
        self.createButton()
        
        self.update()

    def timelinetoVid(self,index):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[index])))
        if(self.playButton.text() == "Pause"):
            self.playButton.setText("Play")
        self.playButton.setEnabled(True)
        for i in range(len(Model.buttonList)):
            Model.buttonList[i].setStyleSheet("border: 2px solid black")
        Model.buttonList[index].setStyleSheet("border: 2px solid red")
            
        


    def timelinetoVid2(self):
        print("vid2")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browse = Window()
    sys.exit(app.exec_())
