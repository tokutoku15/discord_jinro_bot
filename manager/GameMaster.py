import random

class GameMaster():

  def __init__(self, playersDict, roles):
    '''役職の割り当て'''
    for player in playersDict.values():
      random.shuffle(roles)
      player.assignRole(roles.pop(0))
    
    self.playersDict = playersDict
    self.roles = roles

    '''第一夜で襲撃するか'''
    self.oneNightKill = False
    '''第一夜で占うか'''
    self.oneNightExpose = False

    '''人狼の仲間のリスト'''
    # self.werewolfsList = [player for player in self.players if player.getRole().amIWerewolf()]
  
  def getDispPlayers(self):
    arrival = lambda x: '生存' if x else '死亡'
    playerList = [
      '{id:>4} : {name:<12} {isArrival}'.format(
        id=player.getId(),
        name=player.getUserName(),
        isArrival=arrival(player.getArrival()))
      for player in self.playersDict.values()
    ]
    self.playerDisp = '\n'.join(playerList)
    return self.playerDisp
  
  def firstNightCome(self):
    rep = '\n{a:=^50}\n' \
          ':full_moon: みなさん、恐ろしい夜がやってきました\n' \
          '\nこれから夜のアクションを行ってください' \
          '\n夜のアクションはDMで行うことができます'.format(a='')
    return rep

  def nightAct(self, player):
    pass
  
  def dayBreak(self):
    pass

  def vote(self, player, target):
    pass
  
  def gameset(self):
    pass