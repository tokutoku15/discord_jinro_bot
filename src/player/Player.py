class Player():
  def __init__(self, name):
    self.name = name
    self.hasVoted = False
    self.hasActed = False
    self.votedCount = 0
    self.isAlive = True
    '''占い師の占い対象'''
    self.isRevealed = False
    '''騎士の護衛対象'''
    self.isProtected = False
    '''霊媒師の占い対象'''
    self.isDeathAndRevealed = False
    '''人狼の殺害対象'''
    self.willBeKilled = False
  
  def giveDiscRole(self, discRoleName):
    self.discRoleName = discRoleName
  
  def giveDiscRoleId(self, roleId):
    self.roleId = roleId
  
  def giveJob(self, job):
    self.job = job
  
  def finishVote(self):
    self.hasVoted = True
  
  def resetVote(self):
    self.hasVoted = False
  
  def vote(self, target, err=None):
    text = ''
    if not target.isAlive:
      text = '死亡者を選択することはできません\n'
      err = 'error'
    else:
      text = '<@&{target}>を選択しました\n' \
            .format(target=target.roleId)
    return text, err

  def resetCount(self):
    self.votedCount = 0
  
  def voteMe(self):
    self.votedCount += 1
  
  def finishAct(self):
    self.hasActed = True
  
  def resetAct(self):
    self.hasActed = False
  
  def revealMe(self):
    self.isRevealed = True

  def deathRevealMe(self):
    self.isDeathAndRevealed = True

  def protectMe(self):
    self.isProtected = True
  
  def willKill(self):
    self.willBeKilled = True

  def killMe(self):
    self.isAlive = False

  def nextDay(self):
    self.willBeKilled = False
    self.isProtected = False
    self.resetCount()
  
  def giveChannel(self, channel):
    self.myChannel = channel