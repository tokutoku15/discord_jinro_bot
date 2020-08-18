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
    self.targetId = -1
    self.isRevealed = False
    self.hasConfirmed = False
    self.dm = None
  
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

  def votedMe(self):
    self.votedCount += 1
  
  def getVotedCount(self):
    return self.votedCount
  
  def vote(self, targetId):
    self.targetId = targetId
    self.hasVoted = True

  def kill(self):
    self.isAlive = False

  def getIsAlive(self):
    return self.isAlive
  
  def getUserId(self):
    return self.userId
  
  def resetVoteInfo(self):
    self.votedCount = 0
    self.hasVoted = False
    self.targetId = -1
  
  def revealRole(self):
    self.isRevealed = True
  
  def getIsRevealed(self):
    return self.isRevealed
  
  def setDM(self, dm):
    self.dm = dm
  
  def getDM(self):
    return self.dm 
  
  def confirmRole(self):
    self.hasConfirmed = True
  
  def gethasConfirmed(self):
    return self.hasConfirmed