from player.Player import Player

class PlayerManager():

  def __init__(self):
    self.playerIdDict = {}
    self.pnamelist = []
    self.playersDisplay = ''
    self.count = 0
  
  def updatePlayer(self):
    i = 0
    for player in self.playerIdDict.values():
      player.setId(i)
      i += 1
  
  def getPlayersDisplaywithId(self):
    playersDispList = [
      '{id} : {pname}'.format(id=player.getId(), pname=player.getUserName())
      for player in self.playerIdDict.values()
    ]
    text = '\n'.join(playersDispList)
    return text
  
  def getPlayersDisplay(self):
    playersDispList = [
      '{pname}'.format(pname=player.getUserName())
      for player in self.playerIdDict.values()
    ]
    text = '\n'.join(playersDispList)
    return text
  
  def addPlayer(self, pname, userId):
    self.playerIdDict[userId] = Player(pname, userId)
  
  def getPlayerNum(self):
    return len(self.playerIdDict)

  def getPlayerIdDict(self):
    return self.playerIdDict

  def registerDM(self, userId, dm):
    self.playerIdDict[userId].setDM(dm)
  
  def getDMInfo(self, userId):
    return self.playerIdDict[userId].getDM()
  
  def checkAllhasConfirmed(self):
    for player in self.playerIdDict.values():
      if not player.gethasConfirmed():
        return False
    return True