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
  
  def allPlayerHasActed(self):
    for player in self.playerList.values():
      if not player.isAlive:
        continue
      if not player.hasActed:
        return False
    return True
  
  def resetAllPlayerHasActed(self):
    for player in self.playerList.values():
      player.resetAct()
  
  def allPlayerHasVoted(self):
    for player in self.playerList.values():
      if not player.isAlive:
        continue
      if not player.hasVoted:
        return False
    return True

  def resetAllPlayerHasVoted(self):
    for player in self.playerList.values():
      player.resetVote()

  def getAlivePlayerRolesListDisp(self, jobName=None):
    text = ''
    for player in self.playerList.values():
      isWerewolfText = self.isRevealedWerewolf(player, jobName)
      if not isWerewolfText is None:
        isWerewolfText = '[{}]'.format(isWerewolfText)
      else:
        isWerewolfText = ''
      if player.isAlive:
        text += '<@&{}> {}\n'.format(player.roleId, isWerewolfText)
    return text

  def getDeathPlayerRolesListDisp(self, jobName=None):
    text = ''
    for player in self.playerList.values():
      isWerewolfText = self.isRevealedWerewolf(player, jobName)
      if not isWerewolfText is None:
        isWerewolfText = '[{}]'.format(isWerewolfText)
      else:
        isWerewolfText = ''
      if not player.isAlive:
        text += '<@&{}> {}\n'.format(player.roleId, isWerewolfText)
    if not '<@&' in text:
      text = 'なし'
    return text
  
  def isRevealedWerewolf(self, player, jobName):
    text = None
    if jobName == 'fortuneteller':
      if player.isRevealed:
        text = player.job.isWerewolfWithEmoji()
    elif jobName == 'psychic':
      if player.isDeathAndRevealed:
        text = player.job.isWerewolfWithEmoji()
    return text