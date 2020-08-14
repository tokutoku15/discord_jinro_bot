import random

class GameMaster():

  def __init__(self, players, roles):
    '''役職の割り当て'''
    for i, player in enumerate(players):
      random.shuffle(roles)
      player.assignRole(roles.pop(0))
    
    self.players = players
    self.roles = roles
  
  def getDispPlayers(self):
    self.arrival = lambda x: '生存' if x else '死亡'
    self.playerList = [
      '{id:>4} : {name:<12} {isArrival}'.format(id=player.getId(),name=player.getUserName(),isArrival=self.arrival(player.getArrival()))
      for player in self.players
    ]
    self.playerDisp = '\n'.join(self.playerList)
    return self.playerDisp