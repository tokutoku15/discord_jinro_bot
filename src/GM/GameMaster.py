import discord
from src.manager.PlayerManager import PlayerManager
from src.manager.GameStateManager import GameStateManager
from src.manager.JobManager import JobManager

class GameMaster():

  def __init__(self, jinroChannel):
    self.jinroChannel = jinroChannel
    self.stateDisp = {
      'pause' : {
        'display' : 'Bot休止中',
        'commands' : {
          '/setup':'ゲームの立ち上げ'
        }
      },
      'setup' : {
        'display' : 'ゲームのセットアップ',
        'commands' : {
          '/join':'ゲームへ参加', 
          '/exit':'ゲームから退出', 
          '/option':'オプションの変更',
          '/job':'役職の人数の変更', 
          '/start':'ゲームの開始'
        }
      },
      'playing_day' : {
        'display' : '昼のフェーズ',
        'commands' : {
          '/vote' : '対象のプレイヤーに投票'
        }
      },
      'playing_night' : {
        'display' : '夜のフェーズ',
        'commands' : {
          '/act':'役職のアクションの実行'
        }
      },
      'playing_result' : {
        'display' : 'ゲームリザルト',
        'commands' : {},
      },
      'other' : {
        'display' : 'その他',
        'commands' : {
          '/help':'利用可能なコマンドの確認'
        }
      },
    }
    self.initialize()

  def initialize(self):
    self.gameStateManagr = GameStateManager()
    self.playerManager = PlayerManager()
    self.jobManager = JobManager()
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
    description = "<@!{userId}>からゲーム開始が提案されました\n" \
                  "・/join コマンド   : ゲームへ参加\n" \
                  "・/exit コマンド   : ゲームから退出\n" \
                  "・/option コマンド : オプションの変更\n" \
                  "・/job コマンド    : 役職の人数の変更\n" \
                  "・/start コマンド  : ゲームの開始\n" \
                  "・/help コマンド   : 利用可能なコマンドの確認\n" \
                    .format(userId = author.id)
    ret = self.gameOptDisp(description=description)
    return ret
  
  def join(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'setup':
      err = self.getPhaseDisp()+'/joinコマンドは使用できません'
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
      err = self.getPhaseDisp()+'/exitコマンドは使用できません'
      return err
    author = message.author
    self.playerManager.removePlayer(author.id)
    description = "<@!{userId}>がゲームから退出しました" \
                    .format(userId=author.id)
    ret = self.gameOptDisp(description=description)
    return ret
  
  def option(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'setup':
      err = self.getPhaseDisp()+'/optionコマンドは使用できません'
      return err
    mes = message.content.split(' ')
    err = '対象のオプションIDまたはオプションが認識できません\n' \
          '/set [対象のオプションID] [on/off] でルールを設定してください\n' \
          '例: 第一夜の殺害をONにしたい時\n' \
          '**/option 1 on**'
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
  
  def job(self, message):
    if self.jinroChannel != message.channel:
      return
    if self.gameStateManagr.nowState() != 'setup':
      err = self.getPhaseDisp()+'/jobコマンドは使用できません'
      return err
    mes = message.content.split(' ')
    index = 1
    err = '対象の役職IDが認識できません\n' \
          '/job [対象の役職ID] [人数]... で役職の人数を設定してください\n' \
          '複数の役職の人数も設定できます\n' \
          '例: 村人を3人、人狼を2人に設定する時\n' \
          '**/job 0 3 1 2**' 
    if len(mes[index:]) < 2:
      return err
    while len(mes[index:]) >= 2:
      jobId = int(mes[index])
      jobNum = int(mes[index+1])
      if jobId >= len(self.jobManager.jobNumList):
        return err
      self.jobManager.setJobNum(jobId, jobNum)
      index += 2
    ret = self.gameOptDisp()
    return ret

  def getPhaseDisp(self):
    phase = self.gameStateManagr.nowState()
    text = '今のフェーズは{phase}です\n'.format(phase=phase)
    return text

  def gameOptDisp(self, **kwargs):
    description = None
    if 'description' in kwargs.keys():
      description = kwargs['description']
    embed = discord.Embed(title='Jinro Bot', description=description, color=0x2586d0)

    checkMark = lambda x: '✔︎' if x else ' '
    oneNightKill = '`[{}]`ON\n`[{}]`OFF' \
      .format(checkMark(self.oneNightKill), 
              checkMark(not self.oneNightKill))
    embed.add_field(name='[1]第一夜の殺害', value=oneNightKill, inline=True)

    oneNightExpose = '`[{}]`ON\n`[{}]`OFF' \
      .format(checkMark(self.oneNightExpose), 
              checkMark(not self.oneNightExpose))
    embed.add_field(name='[2]第一夜の占い', value=oneNightExpose, inline=True)

    jobNumList = self.jobManager.getJobDispList()
    print(jobNumList)
    embed.add_field(name="役職リスト", value=jobNumList, inline=True)
    
    joiners = self.playerManager.getPlayersListDisp()
    embed.add_field(name='参加者', value=joiners, inline=True)
    return embed

  def help(self, message):
    embed = discord.Embed(title="Help", description="利用できるコマンドは以下の通りです", color=0x2586d0)
    for phase in self.stateDisp.keys():
      text = ''
      if len(self.stateDisp[phase]['commands']) != 0:
        text = '\n'.join([
          '{cmd} : {description}'.format(cmd=cmd, description=description)
          for cmd, description in self.stateDisp[phase]['commands'].items()
        ])
      else:
        text = 'なし'
      embed.add_field(name=self.stateDisp[phase]['display'], value=text, inline=False)
    return embed 
