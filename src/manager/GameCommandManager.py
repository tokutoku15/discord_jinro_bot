import discord
from src.GM.GameMaster import GameMaster
'''
クライアントとコマンドを繋ぐインタフェース的な役割をする
'''
class GameCommandManager():

  def __init__(self, gameChannel):
    self.GM = GameMaster(gameChannel)
    self.isAccept = True
    self.commands = {
      '/setup'  : self.setup,
      '/join'   : self.join,
      '/exit'   : self.exit,
      '/option' : self.option,
      '/time'   : self.time,
      '/job'    : self.job,
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
  
  def option(self, message):
    ret = self.GM.option(message)
    return ret
  
  def time(self, message):
    ret = self.GM.time(message)
    return ret

  def job(self, message):
    ret = self.GM.job(message)
    return ret
  
  def start(self, message):
    ret = self.GM.start(message)
    return ret

  '''
  ゲームアクションコマンド
  '''
  def vote(self, message):
    ret = self.GM.vote(message)
    return ret

  def act(self, message):
    ret = self.GM.act(message)
    return ret

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

  def parseMesAndRunCmd(self, message, ret=None, notification=None):
    mes = message.content.split(' ')
    if mes[0] in self.commands:
      ret, notification = self.commands[mes[0]](message)
    return ret, notification
    