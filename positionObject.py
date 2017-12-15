'''

Fall 2017 CSC 690

File: videoEditor.py

By: Calvin Ip & Jerry AuYeung
Last revised: 12/14/2017

This is an object created to hold the position the videos were placed at,
the duration of each video, and the index of the list of videos.

'''



class positionObject:
    def __init__(self,timepos,index,duration):
        self.timepos = timepos
        self.index = index
        self.duration = duration
    
    def __repr__(self):
        return repr((self.timepos,self.index,self.duration))
