class Player():
  def __init__(self, name):
    self.name = name
    self.hasVoted = False
    self.hasActed = False
    self.votedCount = 0
    '''占い師の占い対象'''
    self.isRevealed = False
    '''騎士の護衛対象'''
    self.isProtected = False
    '''霊媒師の占い対象'''
    self.isDeathAndRevealed = False
    '''人狼の殺害対象'''
    self.willBeKilled = False
  
  def giveDiscRole(self, discRole):
    self.discRole = discRole
  
  def vote(self):
    self.hasVoted = True
  
  def resetVote(self):
    self.hasVoted = False
  
  def act(self):
    self.hasActed = True
  
  def resetAct(self):
    self.hasActed = False
  
  def nextDay(self):
    self.willBeKilled = False
    self.isProtected = False
    self.resetCount()
  
  def resetCount(self):
    self.votedCount = 0
  
  def voteMe(self):
    self.votedCount += 1