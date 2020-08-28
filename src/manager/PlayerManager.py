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
  
  def getAlivePlayerRolesListDisp(self):
    text = ''
    plist = '>\n<@&'.join([
      str(player.roleId)
      for player in self.playerList.values()
      if player.isAlive
    ])
    text += '<@&{}>'.format(plist)
    return text

  def getDeathPlayerRolesListDisp(self):
    text = ''
    deathList = [
      str(player.roleId)
      for player in self.playerList.values()
      if not player.isAlive
    ]
    if len(deathList) == 0:
      text += 'なし'
    else:
      plist = '>\n<@&'.join(deathList)
      text += '<@&{}>'.format(plist)
    return text