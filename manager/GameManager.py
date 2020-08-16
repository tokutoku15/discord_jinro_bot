class GameManager():

  def __init__(self):
    pass

  '''
  それぞれのセリフ(Line)をここでまとめる
  '''
  
  def proposalLine(self, user):
    rep = '{user}から人狼ゲームの提案がされました\n' \
          'ゲームに参加する人は「参加」と発言してください\n' \
            .format(user=user)
    return rep
  
  def joinLine(self, user, displayList):
    rep = '{user}が参加しました\n' \
          '今の参加者は\n' \
          '{a:=^30}\n{displayList}\n{a:=^30}\n' \
          'このメンバーで開始する場合は「確定」と発言してください\n' \
            .format(user=user, displayList=displayList, a='')
    return rep
  
  def decidePlayerLine(self, playerNum, displayList):
    rep = 'このメンバーで確定しました\n' \
          '【参加者{playerNum}名】\n' \
          '{a:=^30}\n{displayList}\n{a:=^30}\n' \
            .format(playerNum=playerNum,displayList=displayList,a='')
    return rep
  
  def roleListLine(self, displayList):
    rep = '役職の人数を決めます\n' \
          '次のリストをコピペして人数を決めて送信してください\n' \
          '{list:=^30}\n{displayList}\n{a:=^33}\n' \
            .format(list='役職リスト', displayList=displayList, a='')
    return rep

  def requestSendAgainLine(self):
    rep = 'プレイヤー数と役職の合計が一致しません\n' \
          'もう一度人数を決めて送信してください\n'
    return rep
  
  def decideRoleNumLine(self, displayList):
    rep = '役職を以下のように設定しました\n' \
          '{list:=^30}\n{displayList}\n{a:=^33}\n' \
            .format(list='役職リスト',displayList=displayList,a='')
    return rep

  def assignRoleLine(self, roleName, roleCamp):
    rep = 'あなたの役職は{roleName}{roleCamp}です\n'.format(roleName=roleName,roleCamp=roleCamp)
    return rep
  
  def finishSendRoleLine(self):
    rep = '役職が決まりました\nDMに役職を送信しました\n'
    return rep