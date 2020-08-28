from src.player.Player import Player

class PlayerManager():
  def __init__(self):
    self.playerList = {}
  
  def addPlayer(self, name, userId):
    player = Player(name)
    self.playerList[userId] = player
  
  def removePlayer(self, userId):
    self.playerList.pop(userId)
  
  def getPlayersListDisp(self):
    text = ''
    if len(self.playerList) == 0:
      text += '参加者0人!'
    else:
      plist = '>\n<@!'.join([
        str(userId)
        for userId in self.playerList.keys()
        ])
      text += '<@!{}>'.format(plist)
    return text
  