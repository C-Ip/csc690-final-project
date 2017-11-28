



class positionObject:
    def __init__(self,timepos,index):
        self.timepos = timepos
        self.index = index
    
    def __repr__(self):
        return repr((self.timepos,self.index))
