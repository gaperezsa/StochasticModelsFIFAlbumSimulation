import random




n = 560
p = 1
P = [pow(1.01,i-1)*p for i in range(0,n)]
P_acumulated = [sum(P[:-n+i]) for i in range(0,n)]

class Agent(): #
    def __init__(self, total, posX, posY):
        self.total = total
        self.obtained = set()
        self.repeated = []
        self.posX = posX
        self.posY = posY
    
    def setPosX(self, posX):
        self.posX = posX
    def setPosY(self, posY):
        self.posY = posY
    def getRepeated(self):
        return self.repeated
    def openEnvelope(self):
        def getRandomSticker():
            rand = random.random(0,1)
            for p in P_acumulated:
                if rand >= p:
                    sticker = P_acumulated.index(p)
                    break
            return sticker
        for i in range(0,5):
            sticker = getRandomSticker()
            if sticker in self.obtained:
                self.repeated.append(sticker)
            else:
                self.obtained.add(sticker)
    
    def addSticker(self,sticker):
        self.obtained.add(sticker)
        
    def removeRepeated(self,sticker):
        self.repeated.remove(sticker)
            
    def trade(self, otherAgent):
        def calculatePrice(stickers):
            return sum([1/P[sticker] for sticker in stickers])
        myRepeated = self.repeated
        peerRepeated = otherAgent.getRepeated()
        needed = []
        neededForPeer = []
        #Check stickers needed that are available in repeated list of peer
        for sticker in peerRepeated:
            if sticker not in self.obtained:
                needed.append(sticker)
        #Check stickers needed for peer that are available in my repeated list
        for sticker in myRepeated:
            if sticker not in otherAgent.obtained:
                neededForPeer.append(sticker)
        needed.sort()
        neededForPeer.sort()
        #CalculatePrice and make deal
        myPrice = calculatePrice(neededForPeer)
        peerPrice = calculatePrice(needed)
        delta = myPrice - peerPrice
        if delta > 0:
            while delta > 0:
                mostValueSticker = neededForPeer.pop(-1)
                myPrice = calculatePrice(neededForPeer)
                peerPrice = calculatePrice(needed)
                delta = myPrice - peerPrice
            neededForPeer.append(mostValueSticker)
        elif delta < 0:
            while delta < 0:
                mostValueSticker = needed.pop(-1)
                myPrice = calculatePrice(neededForPeer)
                peerPrice = calculatePrice(needed)
                delta = myPrice - peerPrice
            needed.append(mostValueSticker)
        
        #Make deal
        for sticker in needed:
            self.addSticker(sticker)
            otherAgent.removeRepeated(sticker)
        for sticker in neededForPeer:
            otherAgent.addSticker(sticker)
            self.removeRepeated(sticker)
        
            
        
        
        
            
              
        
    

def initialize():
    T = [] # Initial values for Time and Space
    X = [] # Initial values for Studio 
    theta = [] # Initial values for features
    E = [] # Initial values for parameters
    L = [] # Initial values for List of Events
    return


def manageTimeAndSpace():
    
    return

def updateSystem():
    return

def updateFeatures():
    return

def updateEventsList():
    return

def event_1():
    X     = updateSystem()
    theta = updateFeatures()
    L     = updateEventsList()
    return
def event_2():
    X     = updateSystem()
    theta = updateFeatures()
    L     = updateEventsList()
    return
def event_3():
    X     = updateSystem()
    theta = updateFeatures()
    L     = updateEventsList()
    return
def event_4():
    X     = updateSystem()
    theta = updateFeatures()
    L     = updateEventsList()
    return
def event_5():
    X     = updateSystem()
    theta = updateFeatures()
    L     = updateEventsList()
    return
def event_6():
    X     = updateSystem()
    theta = updateFeatures()
    L     = updateEventsList()
    return

def generateReport():
    print("Eureka")
    return


if __name__ == 'main':
    Error = 0
    initialize()
    End = False
    while(not End and Error == 0):
        i = manageTimeAndSpace( End , Error )
        if i == 1:
            event_1()
        if i == 2:
            event_2()
        if i == 3:
            event_3()
        if i == 4:
            event_4()
        if i == 5:
            event_5()
        if i == 6:
            event_6()
            
    generateReport()