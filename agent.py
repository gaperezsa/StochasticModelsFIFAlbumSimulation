import random

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
                if rand <= p:
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
        PeersNeeds = []
        #Check stickers needed that are available in repeated list of peer
        for sticker in peerRepeated:
            if sticker not in self.obtained and sticker not in needed:
                needed.append(sticker)
                
        #Check stickers needed for peer that are available in my repeated list
        for sticker in myRepeated:
            if sticker not in otherAgent.obtained and sticker not in PeersNeeds:
                PeersNeeds.append(sticker)
                
        needed.sort()
        PeersNeeds.sort()
        
        #Calculate Price and make deal
        myPrice = calculatePrice(PeersNeeds)
        peerPrice = calculatePrice(needed)
        #Verify fair trade
        delta = myPrice - peerPrice
        if delta > 0:
            while delta > 0:
                mostValueSticker = PeersNeeds.pop(0)
                myPrice = calculatePrice(PeersNeeds)
                peerPrice = calculatePrice(needed)
                delta = myPrice - peerPrice
            PeersNeeds.append(mostValueSticker)
        elif delta < 0:
            while delta < 0:
                mostValueSticker = needed.pop(0)
                myPrice = calculatePrice(PeersNeeds)
                peerPrice = calculatePrice(needed)
                delta = myPrice - peerPrice
            needed.append(mostValueSticker)
        
        #Make deal
        for sticker in needed:
            self.addSticker(sticker)
            otherAgent.removeRepeated(sticker)
        for sticker in PeersNeeds:
            otherAgent.addSticker(sticker)
            self.removeRepeated(sticker)
 