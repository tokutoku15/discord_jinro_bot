class Player():

  '''
  参加順？にidを与える
  '''
  def __init__(self, username, id, userId):
    self.username = username
    self.id = id
    self.userId = userId
    self.votedCount = 0
    self.isArrival = True
  
  def getUserName(self):
    return self.username
  
  def getId(self):
    return self.id
  
  def assignRole(self, role):
    self.role = role
  
  def WhoamI(self):
    return self.role

  def votedMe(self):
    self.votedCount += 1
  
  def getVotedCount(self):
    return self.votedCount
  
  def resetVotedCount(self):
    self.votedCount = 0

  def kill(self):
    self.isArrival = False

  def getArrival(self):
    return self.isArrival
  
  def getUserId(self):
    return self.userId