from abc import ABCMeta, abstractmethod

class Job(metaclass=ABCMeta):

  def __init__(self):
    self.emojiDict = {}

  def setJobName(self, name):
    self.jobName = name
  
  def setJobDispName(self, dispName):
    self.jobDispName = dispName
  
  def setWerewolf(self, isWerewolf):
    self.isWerewolf = isWerewolf
  
  def setJobEmoji(self, emojiDict):
    self.emojiDict = emojiDict
  
  def isWerewolfWithEmoji(self):
    isWerewolfText = ''
    if self.isWerewolf:
      isWerewolfText =  '人狼{emoji}' \
        .format(emoji=self.emojiDict['werewolf'])
    else:
      isWerewolfText = '人間{emoji}' \
        .format(emoji=self.emojiDict['villager'])
    return isWerewolfText

  def getJobNameWithEmoji(self):
    return '{jobName}{emoji}'.format(jobName=self.jobDispName, emoji=self.emojiDict[self.jobName])

  @abstractmethod
  def act(self, target, err=None):
    pass

  @abstractmethod
  def requestAct(self):
    pass