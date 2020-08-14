class Role():

  def __init__(self):
    self.assign = False

  def setDispName(self, name):
    self.name = name
  
  def getDispName(self):
    return self.name

  def setRole(self, role):
    self.role = role
  
  def getRole(self):
    return self.role
  
  def assigning(self):
    self.assign = True
  
  def isAssigned(self):
    return self.assign
  
  def setWerewolf(self, isWerewolf):
    self.isWerewolf = isWerewolf
  
  def amIWerewolf(self):
    return self.isWerewolf