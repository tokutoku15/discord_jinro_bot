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
    '''人狼に昨夜噛まれたプレイヤー'''
    self.killedLastNight = None
    '''人狼リスト'''
    self.werewolfsList = [
      player for player 
      in self.playersDict.values()
      if player.getRole().getRoleName()=='werewolf']
  
  def nextDay(self):
    self.dayCount += 1
  
  def updateDispPlayer(self, author):
    playerRoleList = []
    isWerewolf = lambda x: '人狼' if x else '人間'
    if author.getRole().getRoleName() == 'werewolf':
      for player in self.playersDict.values():
        if author.getUserId() == player.getUserId():
          playerRoleList.append('← あなた')
        elif player.getRole().amIWerewolf():
          playerRoleList.append(f'[{isWerewolf(player.getRole().amIWerewolf())}]')
        else:
          playerRoleList.append(' ')
    elif author.getRole().getRoleName() == 'fortuneteller':
      for player in self.playersDict.values():
        if author.getUserId() == player.getUserId():
          playerRoleList.append('← あなた')
        elif player.getIsRevealed():
          playerRoleList.append(f'[{isWerewolf(player.getRole().amIWerewolf())}]')
        else:
          playerRoleList.append(' ')
    elif author.getRole().getRoleName() == 'psychic':
      for player in self.playersDict.values():
        if author.getUserId() == player.getUserId():
          playerRoleList.append('← あなた')
        elif player.getIsDeathAndRevealed():
          playerRoleList.append(f'[{isWerewolf(player.getRole().amIWerewolf())}]')
    else:
      for player in self.playersDict.values():
        if author.getUserId() == player.getUserId():
          playerRoleList.append('← あなた')
        else:
          playerRoleList.append(' ')

    self.aliveList = [
      '{id:>4} : {name}{role}'.format(
        id=id, name=player.getUserName(),
        role=playerRoleList[id-1])
      for id, player in self.playersDict.items()
      if player.getIsAlive()
    ]
    self.deadList = [
      '{id:>4} : {name:<12}{role}'.format(
        id=id, name=player.getUserName(),
        role=playerRoleList[id-1])
      for id, player in self.playersDict.items()
      if not player.getIsAlive()
    ]

  def getDispDeadorAlive(self, author):
    self.updateDispPlayer(author)
    aliveDisp = '\n'.join(self.aliveList)
    deadDisp = '\n'.join(self.deadList)
    text = '{a:=^30}\n【生存者{alive}名】\n{aliveList}\n{a:=^30}\n' \
            '【死亡者{dead}名】\n{deadList}\n{a:=^30}\n' \
              .format(alive=len(self.aliveList), aliveList=aliveDisp, 
                      dead=len(self.deadList), deadList=deadDisp, a='')
    return text
  
  def ruleDisp(self):
    isOkorNot = lambda x: 'あり' if x else 'なし'
    rep = '{a:=^30}\n【ルール】\n' \
          '・昼の議論の時間：5分\n' \
          '・同票時：全員から再投票\n' \
          '・第1夜での殺害は「{oneNightKill}」\n' \
          '・第1夜での占いは「{oneNightReveal}」\n' \
          '{a:=^30}\n'.format(
            a='', oneNightKill=isOkorNot(self.oneNightKill), 
            oneNightReveal=isOkorNot(self.oneNightReveal))
    return rep
  
  def nightCome(self):
    rep = ':crescent_moon: みなさん、{day}日目の恐ろしい夜がやってきました\n' \
          'これから夜のアクションを行います\n' \
          '夜のアクションはDMで行うことができます'.format(a='', day=self.dayCount)
    return rep

  def nightAct(self, player, actsDisp):
    roleDispName = player.getRole().getDispName()
    roleName = player.getRole().getRoleName()
    rep = 'あなたの役職は{role}です\n'.format(role=roleDispName) 
    # 村人
    if roleName == 'villager':
      rep += '人狼だと思うプレイヤーを選択してください\n'
    # 占い師
    elif roleName == 'fortuneteller':
      if self.dayCount == 1 and not self.oneNightReveal:
        rep += '1日目の占いは行えません\n人狼だと思うプレイヤーを選択してください\n'
      else :
        rep += '占うプレイヤーを選択してください\n'
    # 騎士
    elif roleName == 'night':
      rep += '人狼から守るプレイヤーを選択してください\n'
    # 霊媒師
    elif roleName == 'psychic':
      if len(self.deadList) == 0:
        rep += '人狼だと思うプレイヤーを選択してください\n'
      else:
        rep += '死亡者が人間か人狼かを調べることができます\n' \
               '調べるプレイヤーを選択してください\n'
    # 人狼
    elif roleName == 'werewolf':
      rep += '殺害するプレイヤーを選択してください\n'
      if not self.oneNightKill and self.dayCount == 1:
        rep += '※第1夜の殺害はできません\n'
    rep += '"/act (対象のプレイヤーID)" で役職のアクションを行うことができます\n'
    return rep
  
  def act(self, author, targetId):
    isWerewolf = lambda x: '人狼' if x else '人間'
    for id, player in self.playersDict.items():
      if author.getUserId() == player.getUserId():
        if targetId > len(self.playersDict):
          return ':small_red_triangle: 対象のプレイヤーIDが存在しません\n'
        if targetId == id:
          return ':small_red_triangle: 自分をアクションの対象にできません\n'
        if player.getFinishedAct():
          return ':small_red_triangle: もうアクションを終えています\n'
        # 騎士
        if player.getRole().getRoleName() == 'night':
          if not self.playersDict[targetId].getIsAlive():
            return ':small_red_triangle: {UserName}は死亡しています\n生存者を選択してください\n'.format(UserName=self.playersDict[targetId].getUserName())
          player.actFinish()
          self.playersDict[targetId].IamProtected()
          return ':white_check_mark: {UserName}を守ります\n'.format(UserName=self.playersDict[targetId].getUserName())
        # 占い師
        elif player.getRole().getRoleName() == 'fortuneteller':
          if not self.playersDict[targetId].getIsAlive():
            return ':small_red_triangle: {UserName}は死亡しています\n生存者を占ってください\n'.format(UserName=self.playersDict[targetId].getUserName())
          player.actFinish()
          if self.dayCount == 1 and not self.oneNightReveal:
            self.playersDict[targetId].voteMe()
            return ':white_check_mark: {UserName}を人狼だと選択しました\n'.format(UserName=self.playersDict[targetId].getUserName())
          else:
            self.playersDict[targetId].reveal()
            return ':white_check_mark: {UserName}は{isHuman}です\n' \
              .format(UserName=self.playersDict[targetId].getUserName(), 
              isHuman=isWerewolf(self.playersDict[targetId].getRole().amIWerewolf()))
        # 霊媒師
        elif player.getRole().getRoleName() == 'psychic':
          if self.playersDict[targetId].getIsAlive():
            return ':small_red_triangle: {UserName}は生きています\n死亡者を調べてください\n'.format(UserName=self.playersDict[targetId].getUserName())
          player.actFinish()
          return ':white_check_mark: {UserName}は{isHuman}です\n'.format(UserName=self.playersDict[targetId].getUserName(),
                  isWerewolf=isWerewolf(self.playersDict[targetId].getRole().amIWerewolf()))
        # 人狼
        elif player.getRole().getRoleName() == 'werewolf': 
          if not self.playersDict[targetId].getIsAlive():
            return ':small_red_triangle: {UserName}は死亡しています\n生存者を選択してください\n'.format(UserName=self.playersDict[targetId].getUserName())
          elif self.playersDict[targetId].getRole().getRoleName() == 'werewolf':
            return ':small_red_triangle: 人狼の仲間は選択できません\n村人陣営のプレイヤーを選択してください\n'
          player.actFinish()
          self.playersDict[targetId].setKillFlag()
          return ':white_check_mark: {UserName}を殺害対象に選択しました\n'.format(UserName=self.playersDict[targetId].getUserName())
        # その他
        else:
          player.actFinish()
          self.playersDict[targetId].voteMe()
          return ':white_check_mark: {UserName}を人狼だと選択しました\n'.format(UserName=self.playersDict[targetId].getUserName())

  def nightKill(self):
    for player in self.playersDict.values():
      if player.getWillBeKilled() and not player.getIsProtected():
        player.kill()
        self.killedLastNight = player
    self.killedLastNight = None
  
  def sunRises(self):
    maxVotedCount = -1
    doubtfulPlayer=[]
    for player in self.playersDict.values():
      if maxVotedCount < player.getVotedCount():
        doubtfulPlayer.clear()
        maxVoted = player.getVotedCount()
        doubtfulPlayer.append(player)
      elif maxVotedCount == player.getVotedCount():
        doubtfulPlayer.append(player)
    doubtfulPlayers = '\n'.join([
      '{name}'.format(name=player.getUserName())
      for player in doubtfulPlayer
    ])
    text = '{a:=^30}恐ろしい夜が明け、{day}日目の朝がやってきました\n\n昨晩の犠牲者は・・・\n\n'.format(a='',day=self.dayCount)
    if self.killedLastNight != None:
      text += '{player}です\n'.format(player=self.killedLastNight.getUserName())
    else:
      text += 'いませんでした！人狼は静かに身を潜めたようです\n'
    text += 'そして、にわかに怪しいと思われる人物が浮上しました\n\n'
    text += 'その人物は・・・\n{doubt}\nです\n\n'.format(doubt=doubtfulPlayers)
    text += 'それでは今から人狼を見つけるために話し合いを行ってください\n'
    return text
  
  def finishDiscussion(self):
    text = '話し合いは終了です\n陽は暮れて、今日もひとり容疑者を処分する時間が訪れました\n' \
           'DMで投票を行ってください\n'
    return text


  def vote(self, player, target):
    pass
  
  def gameset(self):
    pass

  def checkAllPlayerHasActed(self):
    for player in self.playersDict.values():
      if not player.getFinishedAct():
        return False
    return True
  
  def checkAllPlayerHasVoted(self):
    for player in self.playersDict.values():
      if not player.gethasVoted():
        return False
    return True