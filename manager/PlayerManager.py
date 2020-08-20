from player.Player import Player

class PlayerManager():

  def __init__(self):
    self.playerIdDict = {}
    self.playerlist = []
    self.playersDisplay = ''
    self.count = 0
  
  def updatePlayer(self):
    i = 0
    for player in self.playerlist:
      i += 1
      self.playerIdDict[i] = player
  
  def getPlayersDisplaywithId(self):
    playersDispList = [
      '{id:>2} : {pname}'.format(id=id, pname=player.getUserName())
      for id, player in self.playerIdDict.items()
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
    if self.isUserIdInPlayerDict(userId):
      pass
    else:
      self.playerlist.append(Player(pname, userId))
      self.updatePlayer()
  
  def getPlayerNum(self):
    return len(self.playerIdDict)

  def getPlayerIdDict(self):
    return self.playerIdDict

  def registerDM(self, userId, dm):
    for player in self.playerIdDict.values():
      if player.getUserId() == userId:
        player.setDM(dm)
  
  def getDMInfo(self, userId):
    for player in self.playerIdDict.values():
      if player.getUserId() == userId:
        return player.getDM()
    return None
  
  def checkAllhasConfirmed(self):
    for player in self.playerIdDict.values():
      if not player.gethasConfirmed():
        return False
    return True
  
  def isUserIdInPlayerDict(self, userId):
    for player in self.playerIdDict.values():
      if player.getUserId() == userId:
        return True
    return False