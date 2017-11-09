from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ExtendedQLabel(QLabel):

    def __init(self,parent):
        QLabel.__init__(self,parent)

    def mouseReleaseEvent(self,e):
        self.emit(SIGNAL('clicked()'))
