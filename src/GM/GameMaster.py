import discord
from src.manager.PlayerManager import PlayerManager
from src.manager.GameStateManager import GameStateManager

class GameMaster():

  def __init__(self, jinroChannel):
    self.jinroChannel = jinroChannel
    self.availableCommands = {
      'pause' : ['/setup'],
      'setup' : ['/join', '/exit', '/setting', '/start'],
      'playing_day' : ['/vote'],
      'playing_night' : ['/act'],
      'playing_result' : [],
      'other' : ['/help'],
    }
    self.stateDisp = {
      'pause' : 'botが休止',
      'setup' : 'ゲームのセットアップ',
      'playing_day' : '昼のフェーズをプレー',
      'playing_night' : '夜のフェーズをプレー',
      'playing_result' : 'ゲームリザルトの表示'
    }
    self.initialize()

  def initialize(self):
    self.gameStateManagr = GameStateManager()
    self.playerManager = PlayerManager()
    self.oneNightKill = False
    self.oneNightExpose = False
  
  def setup(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'pause':
      err = '今は{state}中です\n/setupコマンドは使用できません' \
              .format(state=self.stateDisp[self.gameStateManagr.nowState()])
      return err
    self.gameStateManagr.gameSetup()
    author = message.author
    self.playerManager.addPlayer(author.display_name, author.id)
    description = "<@!{userId}>からゲーム開始が提案されました\n/joinコマンドで参加、/exitコマンドで退室ができます\n" \
                  "参加者が確定したら/startコマンドで始めることができます" \
                    .format(userId = author.id)
    ret = self.gameOptDisp(description=description)
    return ret
  
  def join(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'setup':
      err = '今は{state}中です\n/joinコマンドは使用できません' \
              .format(state=self.stateDisp[self.gameStateManagr.nowState()])
      return err
    author = message.author
    self.playerManager.addPlayer(author.display_name, author.id)
    description = "<@!{userId}>がゲームに参加しました" \
                      .format(userId=author.id)
    ret = self.gameOptDisp(description=description)
    return ret
  
  def exit(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'setup':
      err = '今は{state}中です\n/exitコマンドは使用できません' \
              .format(state=self.stateDisp[self.gameStateManagr.nowState()])
      return err
    author = message.author
    self.playerManager.removePlayer(author.id)
    description = "<@!{userId}>がゲームから退室しました" \
                    .format(userId=author.id)
    ret = self.gameOptDisp(description=description)
    return ret
  
  def setting(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'setup':
      err = '今は{state}中です\n/settingコマンドは使用できません' \
              .format(state=self.stateDisp[self.gameStateManagr.nowState()])
      return err
    mes = message.content.split(' ')
    err = '対象のルールIDまたはオプションが認識できません\n' \
          '/setting [対象のルールID] [on/off] でルールを設定してください\n' \
          '例: 第一夜の殺害をONにしたい時\n' \
          '**/setting 1 on**'
    if len(mes) != 3:
      return err
    if mes[1] == '1':
      if mes[2] == 'on':
        self.oneNightKill = True
      elif mes[2] == 'off':
        self.oneNightKill = False
      else:
        return err
    elif mes[1] == '2':
      if mes[2] == 'on':
        self.oneNightExpose = True
      elif mes[2] == 'off':
        self.oneNightExpose = False
      else:
        return err
    else:
      return err
    ret = self.gameOptDisp()
    return ret

  def gameOptDisp(self, **kwargs):
    description = None
    if 'description' in kwargs.keys():
      description = kwargs['description']
    embed = discord.Embed(title='Jinro Bot', description=description, color=0x2586d0)
    checkMark = lambda x: '✔︎' if x else ' '
    oneNightKill = '`[{}]`ON\n`[{}]`OFF' \
      .format(checkMark(self.oneNightKill), 
              checkMark(not self.oneNightKill))
    embed.add_field(name='1. 第一夜の殺害', value=oneNightKill, inline=True)
    oneNightExpose = '`[{}]`ON\n`[{}]`OFF' \
      .format(checkMark(self.oneNightExpose), 
              checkMark(not self.oneNightExpose))
    embed.add_field(name='2. 第一夜の占い', value=oneNightExpose, inline=True)
    joiners = self.playerManager.getPlayersDisp()
    embed.add_field(name='参加者', value=joiners, inline=False)
    return embed

  def help(self, message):
    embed = discord.Embed(title="Help", description="利用できるコマンドは以下の通りです", color=0x2586d0)
    text = '\n'.join(self.availableCommands['pause'])
    embed.add_field(name="Bot休止中", value=text)
    text = '\n'.join(self.availableCommands['setup'])
    embed.add_field(name="セットアップ", value=text)
    text = '\n'.join(self.availableCommands['playing_day']+self.availableCommands['playing_night'])
    embed.add_field(name="ゲームアクション", value=text)
    text = '\n'.join(self.availableCommands['other'])
    embed.add_field(name="その他", value=text)
    return embed 
