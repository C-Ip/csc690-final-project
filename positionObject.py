



class positionObject:
    def __init__(self,timepos,index,duration):
        self.timepos = timepos
        self.index = index
        self.duration = duration
    
    def __repr__(self):
        return repr((self.timepos,self.index,self.duration))
