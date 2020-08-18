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
    self.oneNightReveal = False

    self.dayCount = 1
  
  def getDayCount(self):
    return self.dayCount
  
  def nextDay(self):
    self.dayCount += 1

  def getDispAlivePlayers(self):
    aliveList = [
      '{id:>4} : {name:<12}'.format(
        id=player.getId(),
        name=player.getUserName())
      for player in self.playersDict.values()
      if player.getIsAlive()
    ]
    aliveDisp = '\n'.join(aliveList)
    text = '{a:=^40}\n【生存者{num}名】\n{aliveList}\n{a:=^40}\n\n' \
              .format(num=len(aliveList), aliveList=aliveDisp, a='')
    return text
  
  def getDispDeadPlayer(self):
    deadList = [
      '{id:>4} : {name:<12}'.format(
        id=player.getId(),
        name=player.getUserName())
      for player in self.playersDict.values()
      if player.getIsAlive()
    ]
    deadDisp = '\n'.join(deadList)
    text = '{a:=40}\n【死亡者{num}名】\n{deadList}\n{a:=^40}\n\n' \
              .format(num=len(deadList), deadList=deadDisp, a='')
    return text
  
  def ruleDisp(self):
    isOkorNot = lambda x: 'あり' if x else 'なし'
    rep = '{a:=^40}\n【ルール】\n' \
          '・昼の議論の時間：5分\n' \
          '・同票時：全員から再投票\n' \
          '・第1夜での殺害は「{oneNightKill}」\n' \
          '・第1夜での占いは「{oneNightReveal}」\n' \
          '{a:=^40}\n'.format(
            a='', oneNightKill=isOkorNot(self.oneNightKill), 
            oneNightReveal=isOkorNot(self.oneNightReveal))
    return rep
  
  def nightCome(self):
    rep = ':crescent_moon: みなさん、{day}日目の恐ろしい夜がやってきました\n' \
          'これから夜のアクションを行います\n' \
          '夜のアクションはDMで行うことができます'.format(a='', day=self.dayCount)
    return rep

  def nightAct(self, player):
    pass
  
  def dayBreak(self):
    pass

  def vote(self, player, target):
    pass
  
  def gameset(self):
    pass