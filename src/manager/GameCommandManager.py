import discord
from src.GM.GameMaster import GameMaster
'''
クライアントとコマンドを繋ぐインタフェース的な役割をする
'''
class GameCommandManager():

  def __init__(self, jinroChannel):
    self.GM = GameMaster(jinroChannel)
    self.isAccept = True
    self.commands = {
      '/setup'  : self.setup,
      '/join'   : self.join,
      '/exit'   : self.exit,
      '/setting': self.setting,
      '/start'  : self.start,
      '/vote'   : self.vote,
      '/act'    : self.act,
      '/help'   : self.help,
    }
  
  '''
  人狼用のテキストチャネルで受け付けるコマンド
  '''
  def setup(self, message):
    ret = self.GM.setup(message)
    return ret

  def join(self, message):
    ret = self.GM.join(message)
    return ret

  def exit(self, message):
    ret = self.GM.exit(message)
    return ret
  
  def setting(self, message):
    ret = self.GM.setting(message)
    return ret
  
  def start(self, message):
    pass

  '''
  ゲームアクションコマンド
  '''
  def vote(self, message):
    pass

  def act(self, message):
    pass

  '''
  その他のコマンド
  '''
  def help(self, message):
    ret = self.GM.help(message)
    return ret 

  def dontAccept(self):
    self.isAccept = False
  
  def readyAccept(self):
    self.isAccept = True

  def parseMesAndRunCmd(self, message, ret=None):
    mes = message.content.split(' ')
    if mes[0] in self.commands:
      ret = self.commands[mes[0]](message)
    return ret
    