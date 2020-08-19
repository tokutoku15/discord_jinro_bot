class Player():

  '''
  参加順？にidを与える
  '''
  def __init__(self, username, userId):
    self.username = username
    self.id = 0
    self.userId = userId
    self.votedCount = 0
    self.isAlive = True
    self.hasVoted = False
    self.hasConfirmed = False
    self.dm = None
    self.hasActed = False
    '''騎士に守護対象'''
    self.isProtected = False
    '''占い師の占い対象'''
    self.isRevealed = False
    '''霊媒師の調査対象'''
    self.isDeathAndRevealed = False
    '''殺害対象に選択されているか'''
    self.willBeKilled = False
  
  def getUserName(self):
    return self.username
  
  def setId(self, id):
    self.id = id
  
  def getId(self):
    return self.id
  
  def assignRole(self, role):
    self.role = role
  
  def getRole(self):
    return self.role

  def voteMe(self):
    self.votedCount += 1
  
  def getVotedCount(self):
    return self.votedCount
  
  def vote(self):
    self.hasVoted = True
  
  def setNotWillBeKilled(self):
    self.willBeKilled = False

  def setKillFlag(self):
    self.willBeKilled = True
  
  def getWillBeKilled(self):
    return self.willBeKilled
  
  def IamProtected(self):
    self.isProtected = True
  
  def isNotProtected(self):
    self.isNotProtected = False
  
  def getIsProtected(self):
    return self.isProtected

  def kill(self):
    self.isAlive = False

  def getIsAlive(self):
    return self.isAlive
  
  def getUserId(self):
    return self.userId
  
  def resetVoteInfo(self):
    self.votedCount = 0
    self.hasVoted = False
  
  def reveal(self):
    if not self.isAlive:
      self.isDeathAndRevealed = True
    else:
      self.isRevealed = True
  
  def getIsRevealed(self):
    return self.isRevealed
  
  def getIsDeathAndRevealed(self):
    return self.isDeathAndRevealed
  
  def setDM(self, dm):
    self.dm = dm
  
  def getDM(self):
    return self.dm 
  
  def confirmRole(self):
    self.hasConfirmed = True
  
  def gethasConfirmed(self):
    return self.hasConfirmed
  
  def gethasVoted(self):
    return self.hasVoted
  
  def resetActed(self):
    self.hasActed = False
  
  def actFinish(self):
    self.hasActed = True
  
  def getFinishedAct(self):
    return self.hasActed