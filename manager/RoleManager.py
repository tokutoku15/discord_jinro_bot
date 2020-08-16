from role.Villager      import Villager
from role.Werewolf      import Werewolf
from role.Night         import Night
from role.FortuneTeller import FortuneTeller
from role.Psychic       import Psychic

class RoleManager():

  def __init__(self):
    self.RoleList = [Villager(), Werewolf(), Night(), FortuneTeller(), Psychic()]
    self.RoleDict = {
      role : 0 for role in self.RoleList
    }
    self.RoleDispNameList = [
      '{role} : {num}'.format(role=role.getDispName(), num=num)
      for role, num in self.RoleDict.items() ]
    self.RolesDisplay = '\n'.join(self.RoleDispNameList)
  
  def getRoleList(self):
    return self.RoleList
  
  def getRolesDisplay(self):
    return self.RolesDisplay
  
  def updateRoleNum(self, listmessage):
    rolenum = 0
    textline = listmessage.split("\n")
    for text in textline:
      for role in self.RoleDict.keys():
        if role.getDispName() in text:
          num = int(text.split(':')[1])
          rolenum += num
          self.RoleDict[role] = num
    self.updateDisp()
    return rolenum

  def updateDisp(self):
    self.RoleDispNameList = [
      '{role} : {num}'.format(role=role.getDispName(), num=num)
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
