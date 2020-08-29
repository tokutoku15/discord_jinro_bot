from abc import ABCMeta, abstractmethod

class Job(metaclass=ABCMeta):

  def __init__(self):
    pass

  def setJobName(self, name):
    self.jobName = name
  
  def setJobDispName(self, dispName):
    self.jobDispName = dispName
  
  def setWerewolf(self, isWerewolf):
    self.isWerewolf = isWerewolf
  
  @abstractmethod
  def act(self, target, err=None):
    pass

  @abstractmethod
  def requestAct(self, emojiDict):
    pass