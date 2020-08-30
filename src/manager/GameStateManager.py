class GameStateManager():
  
  def __init__(self):
    self.stateIndex = 0
    self.states = [
      'pause',
      'setup',
      'playing_day',
      'playing_night',
      'playing_result',
      'playing_dicuss',
    ]
  
  def botPause(self):
    self.stateIndex = 0
  
  def gameSetup(self):
    self.stateIndex = 1 

  def daytime(self):
    self.stateIndex = 2
  
  def nightCome(self):
    self.stateIndex = 3
  
  def gameResult(self):
    self.stateIndex = 4
  
  def discussion(self):
    self.stateIndex = 5
  
  def nowState(self):
    return self.states[self.stateIndex]