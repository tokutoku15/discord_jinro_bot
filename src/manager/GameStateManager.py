class GameStateManager():
  
  def __init__(self):
    self.stateIndex = 0
    self.states = [
      'pause',
      'setup',
      'playing_day',
      'playing_night',
      'playing_result',
    ]
  
  def botPause(self):
    self.stateIndex = 0
  
  def gameSetup(self):
    self.stateIndex = 1 

  def nextDay(self):
    self.stateIndex = 2
  
  def nightCome(self):
    self.stateIndex = 3
  
  def gameResult(self):
    self.stateIndex = 4
  
  def nowState(self):
    return self.states[self.stateIndex]