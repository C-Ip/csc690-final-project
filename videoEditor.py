#!/usr/bin/python3
import sys, os, subprocess, atexit, operator, math
from pygame import mixer
from PyQt5 import QtCore
from operator import itemgetter,attrgetter
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFileDialog, QLineEdit,QSlider
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl, QFileInfo, QTimer
from model import Model
from functools import partial
from tkinter import Tk, Toplevel, Button, Entry, Label
from positionObject import positionObject


class Window(QWidget):
    temptime = 0
    time = 0
    totalDuration = 0
    subtitleIndex = 1
    qp = QPainter()
    
    def __init__(self):
        super().__init__()
        self.title = "Video Editor"
        mixer.pre_init(44100,-16,2,4096)
        mixer.init()
        
        self.display()
        self.initUI()
        self.toolbar()
        self.timeLine()
        self.createButtons()
        self.timeMarks()
        self.importBox()
        self.importPreviewBox()
        #self.createLabel()

        self.timer = QTimer(self)
        self.newtimer = QTimer(self)
        self.subtitleTimer = QTimer(self)
        self.subStopTimer = QTimer(self)
        
        #video player creation, move to own definition later
        self.mediaPlayer = QMediaPlayer(self)
        self.audioPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setGeometry(700,20,600,400)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.videoWidget.setAspectRatioMode(Qt.KeepAspectRatio)
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 50, 1700, 900)
    
    def paintEvent(self,event):
        Window.qp.begin(self)
        self.pen = QPen(Qt.green,5,Qt.SolidLine)
        Window.qp.setPen(self.pen)
        self.drawTimeIndicator(Window.qp)
        Window.qp.end()
    
    def drawTimeIndicator(self,qp):
        if self.totalDuration > 0:
            qp.fillRect(20,585,2,255, Qt.transparent)
        else:
            qp.drawRect(20,585,2,255)
        while self.mediaPlayer.state == QMediaPlayer.PlayingState:
            Window.time += 10
            qp.drawRect(20 * Window.time, 585, 2, 255)
            #qp.fillRect(20 * Window.time - 1, 585, 2, 255)
            
    #creates the box for the import list, default box
    def importBox(self):
        self.importBoxLabel = QLabel(self)
        self.importBoxLabel.setStyleSheet("border: 2px solid black")
        self.importBoxLabel.setGeometry(20,20,300,400)
    #creates the actual box containing the list of imports
    def importBoxList(self,fname):
        Model.importList.append(QPushButton("",self))
        Model.importList[len(Model.videoList)-1].setStyleSheet("border: 2px solid black")
        Model.importList[len(Model.videoList)-1].setText(str(len(Model.importList))+". "+str(fname))
        Model.importList[len(Model.videoList)-1].setGeometry(20,20+(20*(len(Model.videoList)-1)),300,20)
        Model.importList[len(Model.videoList)-1].clicked.connect(partial(self.importClicked, len(Model.videoList)-1))
        Model.importList[len(Model.videoList)-1].show()
    
    def importAudioList(self,aname):
        Model.importAudioList.append(QPushButton("",self))
        Model.importAudioList[len(Model.audioList)-1].setStyleSheet("border: 2px solid black")
        Model.importAudioList[len(Model.audioList)-1].setText(str(len(Model.importAudioList))+". "+str(aname))
        Model.importAudioList[len(Model.audioList)-1].setGeometry(320,20+(20*(len(Model.audioList)-1)),300,20)
        Model.importAudioList[len(Model.audioList)-1].clicked.connect(partial(self.importAudioClicked,len(Model.audioList)-1))
        Model.importAudioList[len(Model.audioList)-1].show()
    
    #creates a box for the preview of each import. TODO: show the thumbnail of each import and details.
    def importPreviewBox(self):
        self.previewBox = QLabel(self)
        self.previewBox.setStyleSheet("Border: 2px solid black")
        self.previewBox.setGeometry(320,20,300,400)
    
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
        self.timeLineLabel.setGeometry(20, 585, 1400, 130)

        # Timeline for subtitles
        self.subTimeLineLabel = QLabel(self)
        self.subTimeLineLabel.setStyleSheet("border: 2px solid black")
        self.subTimeLineLabel.setGeometry(20, 790, 1400, 50)
    
        # timeline audio
        self.audioTimeLine = QLabel(self)
        self.audioTimeLine.setStyleSheet("border: 2px solid black")
        self.audioTimeLine.setGeometry(20,720,1400,60)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0,duration)
        
        if Window.totalDuration == 0:
            self.playTimeLabel = QLabel(self)
        Window.totalDuration += duration
        #print("Total duration: " + str(Window.totalDuration))
        self.seconds = int(math.floor((duration/1000) % 60))
        self.minutes = int(math.floor((duration/60000) % 60))
        self.hours = int(math.floor((duration/3600000) % 24))
        #print("Duration: " + str(duration))

        self.playTimeLabel.setText(str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds))
        self.playTimeLabel.setStyleSheet("font-size: 40px; alignment:center-align")
        self.playTimeLabel.move(450, 500)
        self.playTimeLabel.show()
        #self.createButton()
        

    def createButtons(self):
        #List Titles
        self.videoTitle = QLabel(self)
        self.videoTitle.setText("Video List")
        self.videoTitle.move(20,0)
        
        self.audioTitle = QLabel(self)
        self.audioTitle.setText("Audio List")
        self.audioTitle.move(320,0)
        
        # Play button
        self.playButton = QPushButton("Play", self)
        self.playButton.setStyleSheet("background-color: gray")
        self.playButton.move(700, 500)
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.play)
        
        # Import files button
        self.importButton = QPushButton("Import Videos", self)
        self.importButton.setStyleSheet("background-color: gray")
        self.importButton.move(30, 460)
        self.importButton.clicked.connect(self.importFunction)
        
        # import audio button
        self.importAudioButton = QPushButton("Import Audio",self)
        self.importAudioButton.setStyleSheet("background-color: gray")
        self.importAudioButton.move(30,490)
        self.importAudioButton.clicked.connect(self.importAudioFunction)
        
        self.addSubtitleButton = QPushButton("Add Subtitles", self)
        self.addSubtitleButton.setStyleSheet("background-color: gray")
        self.addSubtitleButton.move(800, 500)
        self.addSubtitleButton.clicked.connect(self.addSubtitles)
        
        self.stopbutton = QPushButton("stop",self)
        self.stopbutton.setStyleSheet("background-color: gray")
        self.stopbutton.move(1000,500)
        self.addSubtitleButton.clicked.connect(self.stopall)

        # Move to timeline button
        self.moveButton = QPushButton("Video to Timeline", self)
        self.moveButton.setStyleSheet("background-color: gray")
        self.moveButton.move(300, 460)
        self.moveButton.clicked.connect(self.createButton)
        self.moveButton.setEnabled(False)
        self.moveButton.setHidden(True)
        
        
        #move audio to timeline
        self.moveAudio = QPushButton("Audio to Timeline",self)
        self.moveAudio.setStyleSheet("background-color:gray")
        self.moveAudio.move(300,490)
        self.moveAudio.clicked.connect(self.createAudioThumbs)
        self.moveAudio.setEnabled(False)
        self.moveAudio.setHidden(True)
        
        self.saveVideo =QPushButton("Save Video",self)
        self.saveVideo.setStyleSheet("background-color:gray")
        self.saveVideo.move(500, 470)
        self.saveVideo.clicked.connect(self.exportFile)
        self.saveVideo.setEnabled(False)
        
        
        
        self.moveOn = QPushButton("Move video",self)
        self.moveOn.setStyleSheet("background-color:gray")
        self.moveOn.move(300, 460)
        self.moveOn.clicked.connect(self.moveOnTimeline)
        self.moveOn.setEnabled(False)
        self.moveOn.setHidden(True)
        
        self.moveAuOn = QPushButton("Move audio",self)
        self.moveAuOn.setStyleSheet("background-color:gray")
        self.moveAuOn.move(300,490)
        self.moveAuOn.clicked.connect(self.moveAudioOnTime)
        self.moveAuOn.setEnabled(False)
        self.moveAuOn.setHidden(True)
        
    
        #qlineedit
        self.positioningRequest = QLineEdit(self)
        self.positioningRequest.setPlaceholderText("Enter Position(seconds)")
        self.positioningRequest.move(150,460)
        self.positioningRequest.resize(150,25)
        self.positioningRequest.setEnabled(False)
        
        self.audioPosition = QLineEdit(self)
        self.audioPosition.setPlaceholderText("Enter Position(seconds)")
        self.audioPosition.move(150,490)
        self.audioPosition.resize(150,25)
        self.audioPosition.setEnabled(False)
        
        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setRange(0,0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setGeometry(20, 585, 1400, 130)
    
    
    def positionChanged(self,position):
        print('Position: ' + str(position))
        self.positionSlider.setValue(position / 40)
        self.positionSlider.show()
    
    
    def setPosition(self,position):
        self.mediaPlayer.setPosition(position)
    
    
        #creates labels/buttons, as the thumbnails of each video imported, TODO:implement with import list as proxy
    def moveOnTimeline(self):
        position = int(self.positioningRequest.text())
    
        currentIndex =  Model.currentVidTimeLineIndex
        Model.buttonList[currentIndex].move(20+(position)*5.5,585)
        Model.positionarray[currentIndex].timepos = position
        self.update()
        Model.od = sorted(Model.positionarray,key=lambda x: x.timepos)
    
    def moveAudioOnTime(self):
        self.soundPosition = int(self.audioPosition.text())
        currentAudioIndex = Model.currentAudioTimeIndex
        Model.audioThumbList[currentAudioIndex].move(20+(self.soundPosition)*5.5,720)
        
        self.update()
    
    
    
    def createAudioThumbs(self):
        
        Model.audioThumbList.append(QPushButton(str(Model.audioCurrent+1),self))
        self.soundPosition = int(self.audioPosition.text())
        self.audioDuration= self.mediaPlayer.duration()


        #Added minutes
        self.audioSeconds = int(round((self.audioDuration/1000)))
        Model.audioThumbList[len(Model.audioThumbList)-1].resize((self.audioSeconds * 5.5),60)
        Model.audioThumbList[len(Model.audioThumbList)-1].setStyleSheet("border: 1px solid black;color:red")
        Model.audioThumbList[len(Model.audioThumbList)-1].move(20+(self.soundPosition)*5.5,720)
        Model.audioThumbList[len(Model.audioThumbList)-1].show()
        Model.audioThumbList[len(Model.audioThumbList)-1].clicked.connect(partial(self.audioTimeLineClicked,len(Model.audioThumbList)-1))
        self.update()

        self.moveAudio.setEnabled(False)


    def createButton(self):
        Model.videoDuration = self.mediaPlayer.duration()
        #Model.videoListLength.append(self.videoDuration)
        Model.buttonList.append(QPushButton(str(Model.current+1),self))
        self.position = int(self.positioningRequest.text())
        Window.totalDuration += self.position * 1000
        
        Model.positionarray.append(positionObject(self.position,Model.current,Model.videoDuration))
        Model.od = sorted(Model.positionarray,key=lambda x: x.timepos)
        
        print(Model.od)

        vidSeconds = int(round((Model.videoDuration/1000) % 60))
        Model.buttonList[len(Model.buttonList)-1].resize((vidSeconds * 5.5),130)
        Model.buttonList[len(Model.buttonList)-1].setStyleSheet("border: 1px solid black; color:red")
        
        Model.buttonList[len(Model.buttonList)-1].move(20+(self.position)*5.5,585)
        Model.buttonList[len(Model.buttonList)-1].clicked.connect(partial(self.timelinetoVid, len(Model.buttonList)-1))
        Model.buttonList[len(Model.buttonList)-1].show()
        
        #writes to a text file to create a list for the ffmpeg comman
        self.file = open(r'bin/text.txt','a+')
        #windows
        #self.file = open(r'bin\text.txt','w+')
        abpath = os.path.abspath("./empty.mp4")
        #windows
        #abpath = os.path.abspath(r'.\empty.avi')
        self.getDelays()
        if len(Model.delayTimes)>0:
            self.file.write("file '" +str(abpath) + "'\n" + "duration " + str(Model.delayTimes[Model.i])+"\n")
            Model.i +=1
        self.file.write("file '"+str(Model.videoList[Model.current])+"'\n")

        self.file.close()
        self.moveButton.setEnabled(False)
        self.playButton.setEnabled(True)
        self.saveVideo.setEnabled(True)
        self.update()
    
    def play(self):
        if Model.timelineState == False:
            if self.mediaPlayer.state() != QMediaPlayer.PlayingState:
                self.mediaPlayer.play()
                self.playButton.setText("Pause")
            else:
                self.mediaPlayer.pause()
            self.playButton.setText("Play")


        # Starts the timer at the last paused time instead of starting at the totalDuration each time.
        if Model.timelineState == True:
            if Model.pausedTime == 0:
                if self.timer.isActive() != True:
                    if Model.tempIndex == len(Model.od):
                        Model.tempIndex = 0
                    if Model.tempIndex < len(Model.od) - 1:
                        if ((Model.od[Model.tempIndex+1].timepos * 1000 )- Model.od[Model.tempIndex].duration) < 0:
                            Model.additionalduration = 0
                        Model.additionalduration = (Model.od[Model.tempIndex+1].timepos * 1000 )- Model.od[Model.tempIndex].duration
                    else:
                        Model.additionalduration = 0
                    # Adds subtitles to preview
                    self.timer.start(Model.od[Model.tempIndex].duration + Model.additionalduration)
                    print("Subtitle Duration: " + str(Model.subtitleDuration))
                    print("Subtitle Start: " + str(Model.subtitleStart))
                    self.subtitleTimer.start(Model.subtitleStart[Model.subtitleIndex] + Model.subtitleDuration[Model.subtitleIndex])
                    print("Timer: " + str(self.timer.remainingTime()))
                    print("Sub Timer: " + str(self.subtitleTimer.remainingTime()))
                    self.mediaPlayer.play()
                    if Model.subtitleIndex < len(Model.subList):
                        self.subtitleTimer.timeout.connect(self.playSubtitles)
                    #
                    if len(Model.audioList) != 0 and self.soundPosition != 0:
                        self.timer.singleShot((self.soundPosition * 1000), self.playAudio)
                    if len(Model.audioList)!=0 and self.soundPosition == 0:
                        self.timer.singleShot(self.soundPosition * 1000, self.playAudio)
                    self.timer.timeout.connect(self.playNext)
                    self.playButton.setText("Pause")
                else:
                    self.mediaPlayer.pause()
                    self.audioPlayer.pause()
                    self.playButton.setText("Play")
                    Model.pausedTime = self.timer.remainingTime()
                    Model.subTimePause = self.subtitleTimer.remainingTime()
                    self.subtitleTimer.stop()
                    self.timer.stop()
                    Model.subList[Model.subtitleIndex - 1].setHidden(True)
            else:
                print("AUSD")
                if self.audioPlayer.state() == QMediaPlayer.PlayingState:
                    self.audioPlayer.pause()
                else:
                    self.audioPlayer.play()
                    
                if self.timer.isActive() != True:
                    self.timer.start(Model.pausedTime)
                    self.subtitleTimer.start(Model.subTimePause)
                    self.mediaPlayer.play()
                    self.playButton.setText("Pause")
                else:
                    self.mediaPlayer.pause()
                    self.playButton.setText("Play")
                    Model.pausedTime = self.timer.remainingTime()
                    self.timer.stop()
                    Model.subTimePause = self.subtitleTimer.remainingTime()
                    self.subtitleTimer.stop()
                    Model.subList[Model.subtitleIndex - 1].setHidden(True)
                    
            self.newtimer.start(1)
            self.newtimer.timeout.connect(self.moveIndicator)
            
        

    def moveIndicator(self):
        Window.temptime = self.newtimer.remainingTime()
  
        Window.qp.drawLine(20 + Window.temptime,585,20 + Window.temptime,840)
        #self.repaint()

        temptime = 0
        time = 0
        temptime = self.newtimer.remainingTime()
        time += temptime
        self.qp.drawLine(20+time,585,20+time,840)
        self.timeLineLabel.repaint()


    def playNext(self):
        Model.tempIndex += 1
        if Model.tempIndex < len(Model.od):
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[Model.od[Model.tempIndex].index])))
            self.mediaPlayer.play()
        else:
            print("video done")
            self.timer.stop()
    def playAudio(self):
        self.audioPlayer.play()
    
    def stopall(self):
        self.timer.stop()
        self.mediaPlayer.stop()
        self.audioPlayer.stop()
    #
    def playSubtitles(self):
        if Model.subtitleIndex == 0:
            Model.subList[Model.subtitleIndex].setHidden(False)
        if Model.subtitleIndex < len(Model.subList) - 1:
            Model.subList[Model.subtitleIndex].setHidden(False)
            Model.subList[Model.subtitleIndex - 1].setHidden(True)
        Model.subtitleIndex += 1
    #   
    
    # import function to get the urls needed to display in the mediaplayer widget
    def importFunction(self):
        Model.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '../desktop','All files(*.jpeg *.mp4 *.mov);;Image files(*.jpeg);;Video Files(*.mp4 *.mov)')
        #windows
        #Model.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '..\desktop','All files(*.jpeg *.mp4 *.mov);;Image files(*.jpeg);;Video Files(*.mp4 *.mov)')
        if Model.fname != '':
            Model.videoList.append(Model.fname)
            # print(Model.videoList)
            fi = QFileInfo(Model.fname)
            base = fi.completeBaseName()
            #print(base)
            self.importBoxList(base)

    def importAudioFunction(self):
        #Model.aname, _ = QFileDialog.getOpenFileName(self, 'Open audio file', '../desktop','All audio files(*.mp3 *.wav)')
        #windows
        Model.aname, _= QFileDialog.getOpenFileName(self, 'Open audio file','..\desktop','All audio files(*.mp3 *.wav)')
        if Model.aname != '':
            Model.audioList.append(Model.aname)
            fi = QFileInfo(Model.aname)
            base = fi.completeBaseName()
            self.importAudioList(base)




    def audioTimeLineClicked(self,index):
        Model.tempIndex = 0
        Model.timelineState = True
        self.cleanImportLists()
        self.cleanTimeline()
        Model.audioThumbList[index].setStyleSheet("border: 2px solid red;color:red")
        if len(Model.buttonList) > 0:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[Model.od[Model.tempIndex].index])))
        self.audioPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.audioList[Model.tempIndex])))
        self.hideTimeButtons()
        self.hideImportButtons()
        self.moveAuOn.setEnabled(True)
        self.moveAuOn.setHidden(False)
        self.enabelSlider()
        self.timer.stop()
    
    

    #clicking each label on the timeline leads here. currently loads video from videourl contained in videoList
    def timelinetoVid(self,index):
        #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[index])))
        n =0
        #self.playButton.setEnabled(True)
        Model.tempIndex = 0
        #highlighting
        Model.timelineState = True
        
        self.cleanImportLists()
        self.cleanTimeline()
        Model.buttonList[index].setStyleSheet("border: 2px solid red;color:red")
        Model.currentVidTimeLineIndex = index
        self.hideImportButtons()
        self.hideTimeButtons()
        self.moveOn.setEnabled(True)
        self.moveOn.setHidden(False)
        self.timer.stop()
        
        self.playButton.setEnabled(True)

        if len(Model.audioThumbList) > 0:
            self.audioPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.audioList[Model.tempIndex])))
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[Model.od[Model.tempIndex].index])))
        if Model.od[0].timepos != 0:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(r"blackvid.mp4")))
        #self.mediaPlayer.play()
        self.enabelSlider()
        
    def getDelays(self):
        if Model.i <len(Model.od)-1:
            Model.delayTimes.append(Model.od[Model.i+1].timepos - ((Model.od[Model.i].duration)/1000 + Model.od[Model.i].timepos))

    def exportFile(self):
        #FFMPEG command, runs the application from the OS to concactenate media files. TODO: fix the usage of different format/codec files
        ffmpeg_command = ["ffmpeg","-y","-f","concat","-safe","0","-i",r"bin/text.txt","-vf","scale=1280:720","-acodec","copy",r"bin/output.mp4"]
        #windows mode
        #ffmpeg_command = ["ffmpeg","-y","-f","concat","-safe","0","-i",r"bin\text.txt","-vf","scale=1280:720","-acodec","copy",r"bin\output.mp4"]
        p = subprocess.call(ffmpeg_command,stdout=subprocess.PIPE)
    
        ffmpeg_audio = ["ffmpeg","-y","-i",r"bin\output.mp4","-itsoffset",str(Model.audioPosition/1000),str(self.importAudioList[0]),"-map", "0:0","-map","1:0","-c:v","copy","-preset","ultrafast","-async","1",r"bin\needSubs.mp4"]
        a = subprocess.call(ffmpeg_audio,stdout=subprocess.PIPE)
        
        ffmpeg_subtitles = ["ffmpeg","-y","-i",r"bin\needSubs.mp4","-i",r"bin\subtitles.srt","-c:v","libx264","-ar","44100","-ac","2","-ab","128k","-strict","-2","-c:s","mov_text","-map","0","-map","1",r"bin\finalVid.mp4"]
        s = subprocess.Popen(ffmpeg_subtitles,stdout=subprocess.PIPE)
        
        out1,err1 = s.communicate()
        out1,err1 = p.communicate()
        out2,err2 = a.communicate()
    

    #highlighting for each item clicked on importlist
    def importClicked(self,index):
        Model.importBoxState = 0
        Model.timelineState = False
        self.cleanImportLists()
        self.cleanTimeline()
        
        Model.importList[index].setStyleSheet("border: 2px solid red")
        self.hideImportButtons()
        self.hideTimeButtons()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[index])))
        self.playButton.setEnabled(True)
        self.moveButton.setEnabled(True)
        self.moveButton.setHidden(False)
        self.positioningRequest.setEnabled(True)
        self.positionSlider.setEnabled(True)
        Model.current = index
        self.enableMove()
        self.positionSlider.setEnabled(True)
        

    def importAudioClicked(self,index):
        Model.timelineState = False
        Model.importBoxState =1
        self.cleanImportLists()
        self.cleanTimeline()
        self.hideImportButtons()
        self.hideTimeButtons()
        self.positionSlider.setEnabled(True)
        
        Model.importAudioList[index].setStyleSheet("border: 2px solid red")
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.audioList[index])))
        #mixer.music.load(Model.audioList[index])
        self.playButton.setEnabled(True)
        self.moveAudio.setEnabled(True)
        self.audioPosition.setEnabled(True)
        self.moveAudio.setHidden(False)
        Model.audioCurrent = index
        self.enableAudio()
        self.positionSlider.setEnabled(True)
    


    def cleanImportLists(self):
        for i in range(len(Model.importList)):
            Model.importList[i].setStyleSheet("border: 2px solid black")
        for i in range(len(Model.importAudioList)):
            Model.importAudioList[i].setStyleSheet("border: 2px solid black")
        self.setFocus()
    def cleanTimeline(self):
        for i in range(len(Model.buttonList)):
            Model.buttonList[i].setStyleSheet("border: 2px solid black")
        for i in range(len(Model.audioThumbList)):
            Model.audioThumbList[i].setStyleSheet("Border:2px solid black")
        self.setFocus()
    
    def timelinetoVid2(self):
        print("vid2")
    


    #creates the timeline
    def timeMarks(self):
        self.markers = QLabel(self)
        self.markers.setGeometry(20, 555, 1400, 30)
        self.markers.setStyleSheet("border: 2px solid black")
        self.markValue = 0
        while self.markValue <= 250:
            self.markerLabel = QLabel(self)
            if self.markValue == 0:
                self.markerLabel.move(20, 555)
            else:
                self.markerLabel.move(20 + (self.markValue * 5.5), 555)
            if (self.markValue % 60 == 0):
                self.markerLabel.setText("|" +str(self.markValue/60)+"0" +"\n" +"|")
            else:
                self.markerLabel.setText("\n" + "|")
            self.markerLabel.setStyleSheet("font: 15px; color: purple")
            self.markValue += 5
        self.markValue = 0
        while self.markValue <= 250:
            self.markerLabel = QLabel(self)
            if self.markValue == 0:
                self.markerLabel.move(20, 710)
            else:
                self.markerLabel.move(20 + (self.markValue * 5.5), 710)
            self.markerLabel.setText("|")
            self.markerLabel.setStyleSheet("font: 15px; color: purple")
            self.markValue += 5

        self.markValue = 0
        while self.markValue <= 250:
            self.markerLabel = QLabel(self)
            if self.markValue == 0:
                self.markerLabel.move(20, 780)
            else:
                self.markerLabel.move(20 + (self.markValue * 5.5), 780)
            self.markerLabel.setText("|")
            self.markerLabel.setStyleSheet("font: 15px; color: purple")
            self.markValue += 5
        




    #deletes videolist file on exit


    # Creates a new window with a text box to enter subtitles
    def addSubtitles(self):
        self.root = Tk()
        self.entry = Entry(self.root)
        self.timePosition = Entry(self.root)
        self.subLength = Entry(self.root)
        
        instructions = Label(self.root, text = "Please enter the text for the subtitles:")
        text = Label(self.root, text = "Time you wish to insert subtitle:")
        length = Label(self.root, text = "Duration of subtitles:")
        
        self.root.title("Add Subtitles")
        self.root.geometry("400x300+500+200")
        addButton = Button(self.root, text="Create Subtitle", command = self.printSubtitles)
        closeButton = Button(self.root, text="Cancel", command = self.destroySecondWindow)
        
        self.entry.pack()
        self.timePosition.pack()
        self.subLength.pack()
        closeButton.pack()
        addButton.pack()
        instructions.pack()
        text.pack()
        length.pack()
        
        instructions.place(x = "80", y = "10")
        self.entry.place(x = "20", y = "50", height = "30", width = "360")
        text.place(x = "100", y = "100")
        self.timePosition.place(x = "150", y = "130", height = "30", width  = "100")
        length.place(x = "150", y = "170")
        self.subLength.place(x = "150", y = "200", height = "30", width = "100")
        closeButton.place(x = "300", y = "230")
        addButton.place(x = "30", y = "230")

        self.root.mainloop()

    # Prints the text entered in the textbox in the second window
    def printSubtitles(self):
        # Labels of subtitles that show on preview
        Model.subList.append(QLabel(self))
        Model.subList[len(Model.subList) - 1].setStyleSheet("border: 2px solid transparent")
        Model.subList[len(Model.subList) - 1].setAlignment(Qt.AlignCenter)
        Model.subList[len(Model.subList) - 1].setGeometry(740, 350, 500, 50)
        
        self.subtitleLabel = QLabel(self)
        Model.subtitleList.append(self.entry.get())
        Model.subList[len(Model.subList) - 1].setText(self.entry.get())
        #Model.subList[len(Model.subList) - 1].setHidden(False)
        Model.subtitleButtonList.append(QPushButton(str(Model.subtitleList[len(Model.subtitleList) - 1]), self))

        self.subtitleDuration = int(self.subLength.get())
        # List of subtitle's duration
        Model.subtitleDuration.append(self.subtitleDuration * 1000)
        Model.subtitleButtonList[len(Model.subtitleList) - 1].resize((self.subtitleDuration * 9),50)
        Model.subtitleButtonList[len(Model.subtitleList) - 1].setStyleSheet("border: 2px solid black")

        # When subtitles start
        subPosition = int(self.timePosition.get())
        Model.subtitleStart.append(subPosition * 1000)
        Model.subtitleButtonList[len(Model.subtitleList) - 1].move(24+(subPosition)*11,790)
        Model.subtitleButtonList[len(Model.subtitleList) - 1].show()
        
        #self.subtitleFile = open(r"bin/subtitles.srt", "a+")
        # Window
        self.subtitleFile = open(r"bin\subtitles.srt", "a+")
        subtitleIndex = 1
        self.subtitleFile.write(str(Window.subtitleIndex) + "\n")
        Window.subtitleIndex += 1
        if subPosition < 10:
            self.subtitleFile.write("00:00:0" + str(subPosition) + ",000 --> ")
            if self.subtitleDuration + subPosition < 10:
                self.subtitleFile.write("00:00:0" + str(self.subtitleDuration + subPosition) + ",000\n")
            if self.subtitleDuration + subPosition >= 10 and self.subtitleDuration + subPosition < 100:
                self.subtitleFile.write("00:00:" + str(self.subtitleDuration + subPosition) + ",000\n")
        if subPosition >= 10 and subPosition <= 59:
            self.subtitleFile.write("00:00:" + str(subPosition) + ",000 --> ")
            if self.subtitleDuration + subPosition >= 60 and self.subtitleDuration + subPosition < 600:
                minutes = int((self.subtitleDuration + subPosition) / 60)
                seconds = (self.subtitleDuration + subPosition) % 60
                if seconds < 10:
                    self.subtitleFile.write("00:0" + str(minutes) + ":0" + str(seconds) + ",000\n")
                else:
                    self.subtitleFile.write("00:0" + str(minutes) + ":" + str(seconds) + ",000\n")
            else:
                self.subtitleFile.write("00:00:" + str(self.subtitleDuration + subPosition) + ",000\n")
            
        self.subtitleFile.write(self.entry.get() + ("\n" * 2))
        self.subtitleFile.close()

        self.destroySecondWindow()

    def hideTimeButtons(self):
        self.moveButton.setHidden(True)
        self.moveButton.setEnabled(False)
        self.moveAudio.setHidden(True)
        self.moveAudio.setEnabled(False)
    
    def hideImportButtons(self):
        self.moveOn.setHidden(True)
        self.moveOn.setEnabled(False)
        self.moveAuOn.setHidden(True)
        self.moveAuOn.setEnabled(False)
    
    def enableMove(self):
        self.moveButton.setEnabled(True)
    
    def enableAudio(self):
        self.moveAudio.setEnabled(True)
    
    
    def enabelSlider(self):
        self.positionSlider.setEnabled(True)
    
    # Destroys the second window
    def destroySecondWindow(self):
        self.root.destroy()

    #deletes videolist file on exit
    @atexit.register
    def goodbye():
        file = open('bin/text.txt','w+')
        #windows
        #file = open('bin\text.txt','w+')
        file.truncate()
        #windows
        """
        if os.path.isfile('bin\output.mp4'):
            os.remove('bin\output.mp4')
        #if os.path.isfile('bin/output.mp4'):
            #os.remove('bin/output.mp4')
        else:
            print("files clean!")
        """
if __name__ == '__main__':
    app = QApplication(sys.argv)
    browse = Window()
sys.exit(app.exec_())
