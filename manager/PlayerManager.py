from player.Player import Player

class PlayerManager():

  def __init__(self):
    self.pnamelist = []
    self.playerlist = []
    self.playersDisplay = ''
  
  def decidePlayer(self):
    self.playerlist = [Player(self.pnamelist[i][0], i, self.pnamelist[i][1]) for i in range(0, len(self.pnamelist))]
    self.playersDisplay = '\n'.join([
      '{id} : {playername}'.format(id=self.playerlist[i].getId(), playername=self.playerlist[i].getUserName())
      for i in range(0, len(self.playerlist))
    ])
  
  def getPlayerList(self):
    return self.playerlist
  
  def getPlayersDisplay(self):
    return self.playersDisplay
  
  def addPlayer(self, pname, userId):
    self.pnamelist.append((pname, userId))

