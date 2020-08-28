class Player():
  def __init__(self, name):
    self.name = name
    self.hasVoted = False
    self.hasActed = False
  
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
  