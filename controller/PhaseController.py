from controller.phase import phase
from controller.phase import gamePhase

class PhaseController():

  def __init__(self):
    '''
    フェーズ
      'pause':休止中、メンションでinvitationに移行
      'invitation':プレイヤーの決定、確定行動でpreparationに移行
      'preparation':役職などのルールの決定、確定行動でnightに移行
      'playing':ゲーム本編、決着がつくとresultへ
      'result':リザルト、pauseやinvitationへ移行可能
    '''
    self.phase = phase[0]
  
  def pause(self):
    self.phase = phase[0]

  def invitation(self):
    self.phase = phase[1]
  
  def preparation(self):
    self.phase = phase[2]
  
  def playing(self):
    self.phase = phase[3]
  
  def result(self):
    self.phase = phase[4]

  def nightCome(self):
    self.phase = gamePhase[0]
  
  def sunRises(self):
    self.phase = gamePhase[1]
  
  def getPhase(self):
    return self.phase