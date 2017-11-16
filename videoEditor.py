#!/usr/bin/python3
import sys, os, subprocess, atexit
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl, QFileInfo, QTime
from model import Model
from functools import partial
from tkinter import Tk, Toplevel, Button, Entry, Label


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
        self.timeMarks()
        self.importBox()
        self.importPreviewBox()
        #self.createLabel()
        
        #video player creation, move to own definition later
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setGeometry(700,20,600,400)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.videoWidget.setAspectRatioMode(Qt.KeepAspectRatio)
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 50, 1700, 900)
    
    #creates labels/buttons, as the thumbnails of each video imported, TODO:implement with import list as proxy
    def createButton(self):
        videoDuration = self.mediaPlayer.duration()
        Model.buttonList.append(QPushButton(str(len(Model.videoList)),self))
        Model.buttonList[len(Model.videoList)-1].move(20+(150*(len(Model.videoList)-1)),625)
        #print("Video duration: " + str(self.mediaPlayer.duration()))
        if videoDuration >= 5000:
            vidSeconds = int(round((videoDuration/1000) % 60))
            print(str(vidSeconds))
            Model.buttonList[len(Model.videoList)-1].resize(24 + (vidSeconds * 9),130)
        Model.buttonList[len(Model.videoList)-1].setStyleSheet("border: 2px solid black")
        index = 0
        Model.buttonList[len(Model.videoList)-1].clicked.connect(partial(self.timelinetoVid, len(Model.videoList)-1))
        Model.buttonList[len(Model.videoList)-1].show()
    
    #creates the box for the import list, default box
    def importBox(self):
        self.importBoxLabel = QLabel(self)
        self.importBoxLabel.setStyleSheet("border: 2px solid black")
        self.importBoxLabel.setGeometry(20,20,300,400)
    #creates the actual box containing the list of imports
    def importBoxList(self,fname):
        Model.importList.append(QPushButton("",self))
        Model.importList[len(Model.videoList)-1].setStyleSheet("border: 2px solid black")
        Model.importList[len(Model.videoList)-1].setText(str(len(Model.importList)-1)+". "+str(fname))
        Model.importList[len(Model.videoList)-1].setGeometry(20,20+(20*(len(Model.videoList)-1)),300,20)
        Model.importList[len(Model.videoList)-1].clicked.connect(partial(self.importClicked, len(Model.videoList)-1))
        Model.importList[len(Model.videoList)-1].show()
    
    #creates a box for the preview of each import. TODO: show the thumbnail of each import and details.
    def importPreviewBox(self):
        self.previewBox = QLabel(self)
        self.previewBox.setStyleSheet("Border: 2px solid black")
        self.previewBox.setGeometry(320,20,300,400)
    
    
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
        self.timeLineLabel.setGeometry(20, 625, 1400, 130)

        # Timeline for subtitles
        self.subTimeLineLabel = QLabel(self)
        self.subTimeLineLabel.setStyleSheet("border: 2px solid black")
        self.subTimeLineLabel.setGeometry(20, 770, 1400, 80)

    def durationChanged(self, duration):
        if Window.totalDuration == 0:
            self.playTimeLabel = QLabel(self)
        Window.totalDuration += duration
        #print("Total duration: " + str(Window.totalDuration))
        self.seconds = int(round((duration/1000) % 60))
        self.minutes = int(round((duration/60000) % 60))
        self.hours = int(round((duration/3600000) % 24))
        #print("Duration: " + str(duration))
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
        self.createButton()
        

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
            
        self.addSubtitleButton = QPushButton("Add Subtitles", self)                                          
        self.addSubtitleButton.setStyleSheet("background-color: gray")
        self.addSubtitleButton.move(800, 500)
        self.addSubtitleButton.clicked.connect(self.addSubtitles)

        # Move to timeline button
        self.moveButton = QPushButton("Move to Timeline", self)
        self.moveButton.setStyleSheet("background-color: gray")
        self.moveButton.move(400, 500)

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
        '''
        if self.mediaPlayer.state() != QMediaPlayer.PlayingState:
            self.mediaPlayer.play()
            self.playButton.setText("Pause")
            while self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                Window.totalDuration -= 1
                if Window.totalDuration == 60000:
                    self.mediaPlayer.pause()
                    self.playButton.setText("Play")
                    break
        '''
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playButton.setText("Pause")
            
    # import function to get the urls needed to display in the mediaplayer widget
    def importFunction(self):
        #Model.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '../desktop','All files(*.jpeg *.mp4 *.mov);;Image files(*.jpeg);;Video Files(*.mp4 *.mov)')
        #windows
        Model.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '..\desktop','All files(*.jpeg *.mp4 *.mov);;Image files(*.jpeg);;Video Files(*.mp4 *.mov)')
        if Model.fname != '':
            Model.videoList.append(Model.fname)
        
        # this part changes the url into just the filename to be used in the import list
        fi = QFileInfo(Model.fname)
        base = fi.completeBaseName()
        #self.createButton()
        self.importBoxList(base)
        
        #writes to a text file to create a list for the ffmpeg comman
        #self.file = open(r'bin/text.txt','w+')
        #windows
        self.file = open(r'bin\text.txt','w+')
        
        for item in Model.videoList:
            self.file.write("file "+"'" + "%s'\n" %item)
        #print (str(item))
        self.file.close()
        
        currentdir = os.getcwd()
        #FFMPEG command, runs the application from the OS to concactenate media files. TODO: fix the usage of different format/codec files
        #ffmpeg_command = ["ffmpeg","-y","-f","concat","-safe","0","-i",r"bin/text.txt","-vf","scale=1280:720","-acodec","copy",r"bin/output.mp4"]
        #windows mode
        ffmpeg_command = ["ffmpeg","-y","-f","concat","-safe","0","-i",r"bin\text.txt","-vf","scale=1280:720","-acodec","copy",r"bin\output.mp4"]
        p = subprocess.Popen(ffmpeg_command,stdout=subprocess.PIPE)
        out1,err1 = p.communicate()
        
        
        #delete this for fix
        #abpath = os.path.abspath(r'bin/output.mp4')
        #windows mode
        abpath = os.path.abspath(r'bin\output.mp4')
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(abpath)))
        self.playButton.setEnabled(True)
        self.update()
            
    #clicking each label on the timeline leads here. currently loads video from videourl contained in videoList
    def timelinetoVid(self,index):
        #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(Model.videoList[index])))
        
        if self.playButton.text() == "Pause":
            self.playButton.setText("Play")
    
        #self.playButton.setEnabled(True)

        #highlighting
        for i in range(len(Model.buttonList)):
            Model.buttonList[i].setStyleSheet("border: 2px solid black")
        Model.buttonList[index].setStyleSheet("border: 2px solid red")
       

    #highlighting for each item clicked on importlist
    def importClicked(self,index):
        for i in range(len(Model.importList)):
            Model.importList[i].setStyleSheet("border: 2px solid black")
        Model.importList[index].setStyleSheet("border: 2px solid red")
            
            

    def timelinetoVid2(self):
        print("vid2")
        
    #creates the timeline
    def timeMarks(self):
        self.markers = QLabel(self)
        self.markers.setGeometry(20, 595, 1400, 30)
        self.markers.setStyleSheet("border: 2px solid black")
        self.markValue = 0
        while self.markValue <= 120:
            self.markerLabel = QLabel(self)
            if self.markValue == 0:
                self.markerLabel.move(20, 600)
            else:
                self.markerLabel.move(20 + (self.markValue * 11), 600)
            self.markerLabel.setText(str(self.markValue) + "\n" + "|")
            self.markerLabel.setStyleSheet("font: 20px")
            self.markValue += 5

    #deletes videolist file on exit

    
    # Creates a new window with a text box to enter subtitles
    def addSubtitles(self):
        self.root = Tk()
        self.entry = Entry(self.root)
        self.timePosition = Entry(self.root)
        instructions = Label(self.root, text = "Please enter the text for the subtitles:")
        text = Label(self.root, text = "Time you wish to insert subtitle:")
        self.root.title("Add Subtitles")
        self.root.geometry("400x300+500+200")
        addButton = Button(self.root, text="Create Subtitle", command = self.printSubtitles)
        closeButton = Button(self.root, text="Cancel", command = self.destroySecondWindow)
        self.entry.pack()
        self.timePosition.pack()
        closeButton.pack()
        addButton.pack()
        instructions.pack()
        text.pack()
        instructions.place(x = "80", y = "10")
        self.entry.place(x = "20", y = "50", height = "30", width = "360")
        text.place(x = "100", y = "100")
        self.timePosition.place(x = "150", y = "130", height = "30", width  = "100")
        closeButton.place(x = "300", y = "180")
        addButton.place(x = "30", y = "180")

        self.root.mainloop()

    # Prints the text entered in the textbox in the second window
    def printSubtitles(self):
        self.subtitleLabel = QLabel(self)
        self.subtitleLabel.setGeometry(20, 770, 40, 80)
        self.subtitleLabel.setStyleSheet("border: 2px solid red")
        self.subtitleLabel.setText(self.entry.get())
        self.subtitleLabel.show()

        #self.subtitleFile = open(r"bin/subtitles.srt", "a+")
        # Window
        self.subtitleFile = open(r"bin\subtitles.srt", "a+")
        self.subtitleFile.write(self.entry.get() + "\n")
        self.subtitleFile.close()

        self.destroySecondWindow()

    # Destroys the second window
    def destroySecondWindow(self):
        self.root.destroy()

    @atexit.register
    def goodbye():
        #file = open('bin/text.txt','w+')
        #windows
        file = open('bin\text.txt','w+')
        file.truncate()
        #os.remove('bin/output.mp4')
        #windows mode
        os.remove('bin\output.mp4')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    browse = Window()
    sys.exit(app.exec_())
