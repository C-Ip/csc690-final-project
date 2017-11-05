#!/usr/bin/python3

import sys, os, cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
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
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 50, 1700, 850)

    def display(self):
        self.displayLabel = QLabel(self)
        self.displayLabel.setStyleSheet("border: 2px solid black")
        self.displayLabel.setGeometry(500, 20, 600, 400)

    def toolbar(self):
        self.toolbarLabel = QLabel(self)
        self.toolbarLabel.setStyleSheet("border: 2px solid black")
        self.toolbarLabel.setGeometry(20, 450, 1600, 100)

    def timeLine(self):
        self.timeLineLabel = QLabel(self)
        self.timeLineLabel.setStyleSheet("border: 2px solid black")
        self.timeLineLabel.setGeometry(20, 560, 1600, 130)

        # Timeline for subtitles
        self.subTimeLineLabel = QLabel(self)
        self.subTimeLineLabel.setStyleSheet("border: 2px solid black")
        self.subTimeLineLabel.setGeometry(20, 700, 1600, 130)

    def createButtons(self):
        # Play button
        self.playButton = QPushButton("Play", self)
        self.playButton.setStyleSheet("background-color: gray")
        self.playButton.move(700, 500)

        # Pause button
        self.pauseButton = QPushButton("Pause", self)
        self.pauseButton.setStyleSheet("background-color: gray")
        self.pauseButton.move(800, 500)

        # Import files button
        self.importButton = QPushButton("Import", self)
        self.importButton.setStyleSheet("background-color: gray")
        self.importButton.move(30, 460)

        # Change to fullscreen button
        self.fullScreenButton = QPushButton("Fullscreen", self)
        self.fullScreenButton.setStyleSheet("background-color: gray")
        self.fullScreenButton.move(1000, 380)

        # Turn on/off subtitle button
        self.subtitleButton = QPushButton("Subtitle ON/OFF", self)
        self.subtitleButton.setStyleSheet("background-color: gray")
        self.subtitleButton.move(900, 500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browse = Window()
    sys.exit(app.exec_())
