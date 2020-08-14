from role.Villager      import Villager
from role.Werewolf      import Werewolf
from role.Night         import Night
from role.FortuneTeller import FortuneTeller
from role.Psychic       import Psychic

class RoleManager():

  
  def __init__(self):
    self.RoleList = [Villager(), Werewolf(), Night(), FortuneTeller(), Psychic()]
    isWerewolf = lambda amIwerewolf: '(人狼陣営)' if amIwerewolf else '(村人陣営)'
    self.RoleDict = {
      role.getDispName() : 0 for role in self.RoleList
    }
    self.RoleDispNameList = [
      '{role} : {num}'.format(role=role, num=num)
      for role, num in self.RoleDict.items()
      ]
    self.RolesDisplay = '\n'.join(self.RoleDispNameList)
  
  def getRoleList(self):
    return self.RoleList
  
  def getRolesDisplay(self):
    return self.RolesDisplay
  
  def updateRoleNum(self, listmessage):
    textline = listmessage.split("\n")
    for text in textline:
      for roleDispName in self.RoleDict.keys():
        if roleDispName in text:
          num = text.split(':')[1]
          self.RoleDict[roleDispName] = int(num)
    self.updateDisp()

  def updateDisp(self):
    self.RoleDispNameList = [
      '{role} : {num}'.format(role=role, num=num)
      for role, num in self.RoleDict.items()
      ]
    self.RolesDisplay = '\n'.join(self.RoleDispNameList)
  
  def generateRoleStack(self):
    self.RoleStack = []
    for role, num in self.RoleDict.items():
      for _ in range(num):
        self.RoleStack.append(role)

  def getRoleStack(self):
    return self.RoleStack
