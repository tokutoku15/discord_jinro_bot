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
    '''生存者と死亡者リスト'''
    self.aliveList = []
    self.deadList = []
  
  def getDayCount(self):
    return self.dayCount
  
  def nextDay(self):
    self.dayCount += 1
  
  def updateDispPlayer(self):
    self.aliveList = [
      '{id:>4} : {name:<12}'.format(
        id=player.getId(),
        name=player.getUserName())
      for player in self.playersDict.values()
      if player.getIsAlive()
    ]
    self.deadList = [
      '{id:>4} : {name:<12}'.format(
        id=player.getId(),
        name=player.getUserName())
      for player in self.playersDict.values()
      if not player.getIsAlive()
    ]

  def getDispDeadorAlive(self):
    self.updateDispPlayer()
    aliveDisp = '\n'.join(self.aliveList)
    deadDisp = '\n'.join(self.deadList)
    text = '{a:=^40}\n【生存者{alive}名】\n{aliveList}\n{a:=^40}\n' \
            '【死亡者{dead}名】\n{deadList}\n{a:=^40}\n' \
              .format(alive=len(self.aliveList), aliveList=aliveDisp, 
              dead=len(self.deadList), deadList=deadDisp, a='')
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
    roleDispName = player.getRole().getDispName()
    roleName = player.getRole().getRoleName()
    rep = 'あなたの役職は{role}です\n'.format(role=roleDispName) 
    if roleName == 'villager':
      rep += '人狼だと思うプレイヤーを選択してください\n'
    elif roleName == 'fortuneteller':
      rep += '占うプレイヤーを選択してください\n'
    elif roleName == 'night':
      rep += '人狼から守るプレイヤーを選択してください\n'
    elif roleName == 'psychic':
      if len(self.deadList) == 0:
        rep += '人狼だと思うプレイヤーを選択してください\n'
      else:
        rep += '死亡者の役職を調べることができます\n' \
               '役職を調べるプレイヤーを選択してください\n'
    elif roleName == 'werewolf':
      rep += '殺害するプレイヤーを選択してください\n'
      if not self.oneNightKill:
        rep += '※第1夜の殺害はできません'
    return rep
  
  def dayBreak(self):
    pass

  def vote(self, player, target):
    pass
  
  def gameset(self):
    pass