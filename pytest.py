class Player():
  def __init__(self, gender, age):
    self.gender = gender
    self.age = age
  
  def birthday(self):
    self.age += 1

class BaseClass():
  def __init__(self):
    pass

  def test_function(self):
    pass

class ChildClass(BaseClass):
  def test_function(self):
    print('ChildClass')

def main():
  playerList = [
    Player('male', 21), 
    Player('female', 19),
  ]

  playerTuple = (
    Player('male', 15),
    Player('male', 30)
  )

  print('playerList')
  for player in playerList:
    print(player.gender, player.age)
  print('playerTuple')
  for player in playerTuple:
    print(player.gender, player.age)
  playerList[1].birthday()
  playerTuple[1].birthday()
  print('playerList')
  for player in playerList:
    print(player.gender, player.age)
  print('playerTuple')
  for player in playerTuple:
    print(player.gender, player.age)
  
  playerList[0] = Player('female', 12)
  # playerTuple[0] = Player('female', 25)

  child = ChildClass()
  child.test_function()

  from src.manager.CommandManager import CommandManager
  commandManager = CommandManager()
  if '/setup ' in commandManager.availableCommands['pause']:
    print('ok')

if __name__=="__main__":
  main()