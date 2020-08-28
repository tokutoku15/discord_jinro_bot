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
  
  def vote(self, targetId):
    text = '<@!{target}>に投票しました\n' \
            .format(target=targetId)
    return text
  
  @abstractmethod
  def act(self):
    pass