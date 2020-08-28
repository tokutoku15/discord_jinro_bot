import random
import discord
from src.manager.PlayerManager import PlayerManager
from src.manager.GameStateManager import GameStateManager
from src.manager.JobManager import JobManager

class GameMaster():

  def __init__(self, gameChannel):
    self.gameChannel = gameChannel
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
          '/time' : '話し合いの時間の変更',
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
    self.dayCount = 1
    self.discussTime = 5
    self.gameStateManager = GameStateManager()
    self.playerManager = PlayerManager()
    self.jobManager = JobManager()
    self.oneNightKill = False
    self.oneNightReveal = False
  
  '''
  コマンド毎の処理
  エラーハンドリング時
  return err, 'error'
  成功時
  return ret, 'command_name'
  '''
  def setup(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'pause':
      err = self.getPhaseDisp() + '/setupコマンドは使用できません'
      return err, 'error'
    self.gameStateManager.gameSetup()
    author = message.author
    self.playerManager.addPlayer(author.display_name, author.id)
    description = "<@!{userId}>からゲーム開始が提案されました\n利用可能なコマンド\n" \
                    .format(userId = author.id)
    description += '\n'.join([
      '{cmd} : {desc}'.format(cmd=cmd,desc=desc)
      for cmd, desc in self.stateDisp['setup']['commands'].items()
    ])
    ret = self.gameOptDisp(description=description)
    return ret, 'setup'
  
  '''joinコマンド'''
  def join(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseDisp()+'/joinコマンドは使用できません'
      return err, 'error'
    author = message.author
    self.playerManager.addPlayer(author.display_name, author.id)
    description = "<@!{userId}>がゲームに参加しました" \
                      .format(userId=author.id)
    ret = self.gameOptDisp(description=description)
    return ret, 'join'
  
  '''exitコマンド'''
  def exit(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseDisp()+'/exitコマンドは使用できません'
      return err, 'error'
    author = message.author
    self.playerManager.removePlayer(author.id)
    description = "<@!{userId}>がゲームから退出しました" \
                    .format(userId=author.id)
    ret = self.gameOptDisp(description=description)
    return ret, 'exit'
  
  '''optionコマンド'''
  def option(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseDisp()+'/optionコマンドは使用できません'
      return err, 'error'
    mes = message.content.split(' ')
    err = '対象のオプションIDまたはオプションが認識できません\n' \
          '/set [対象のオプションID] [on/off] でルールを設定してください\n' \
          '例: 第一夜の殺害をONにしたい時\n' \
          '**/option 1 on**'
    if len(mes) != 3:
      return err, 'error'
    if mes[1] == '1':
      if mes[2] == 'on':
        self.oneNightKill = True
      elif mes[2] == 'off':
        self.oneNightKill = False
      else:
        return err, 'error'
    elif mes[1] == '2':
      if mes[2] == 'on':
        self.oneNightReveal = True
      elif mes[2] == 'off':
        self.oneNightReveal = False
      else:
        return err, 'error'
    else:
      return err, 'error'
    ret = self.gameOptDisp()
    return ret, 'option'
  
  '''timeコマンド'''
  def time(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseDisp()+'/timeコマンドは使用できません'
      return err, 'error'
    mes = message.content.split(' ')
    err = '時間を正しく設定できていません\n' \
          '/time [時間(分)] で話し合いの時間を設定してください(最大20分、最小1分)\n' \
          '例: 話し合いの時間を3分にしたい時\n' \
          '**/time 3**'
    if len(mes) != 2:
      return err, 'error'
    if int(mes[1]) <= 0 or 20 <= int(mes[1]):
      return err, 'error'
    self.discussTime = int(mes[1])
    embed = self.gameOptDisp()
    return embed, 'time'
  
  '''jobコマンド'''
  def job(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseDisp()+'/jobコマンドは使用できません'
      return err, 'error'
    mes = message.content.split(' ')
    index = 1
    err = '対象の役職IDが認識できません\n' \
          '/job [対象の役職ID] [人数]... で役職の人数を設定してください\n' \
          '複数の役職の人数も設定できます\n' \
          '例: 村人を3人、人狼を2人に設定する時\n' \
          '**/job 0 3 1 2**' 
    if len(mes[index:]) < 2:
      return err, 'error'
    while len(mes[index:]) >= 2:
      jobId = int(mes[index])
      jobNum = int(mes[index+1])
      if jobId >= len(self.jobManager.jobNumList):
        return err, 'error'
      self.jobManager.setJobNum(jobId, jobNum)
      index += 2
    ret = self.gameOptDisp()
    return ret, 'job'
  
  '''startコマンド'''
  def start(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseDisp()+'/startコマンドは使用できません'
      return err, 'error'
    jobNumSum = sum(list(self.jobManager.jobNumList.values()))
    playerNum = len(self.playerManager.playerList)
    if jobNumSum != playerNum:
      err = '参加者の人数と役職の合計人数が一致しません\n' \
            '/jobコマンドで役職の人数を変更してください\n'
      return err, 'error'
    ret = '役職の割り振りとチャンネルの作成を行います\n'
    self.gameStateManager.nightCome()
    self.giveRoleAndJob()
    return ret, 'start'
    
  '''helpコマンド'''
  def help(self, message):
    if self.gameChannel != message.channel:
      return None, 'error'
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
    return embed, 'help'

  '''
  ユーティリティ関数
  '''
  def giveRoleAndJob(self):
    for player in self.playerManager.playerList.values():
      roleName = 'player-{}'.format(player.name)
      jobs = self.jobManager.getJobStack()
      random.shuffle(jobs)
      player.giveDiscRole(roleName)
      player.giveJob(jobs.pop(0))

  def getPhaseDisp(self):
    phase = self.gameStateManager.nowState()
    phaseText = self.stateDisp[phase]['display']
    text = '今のフェーズは{phase}です\n'.format(phase=phaseText)
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
    embed.add_field(name='[1]第1夜の殺害', value=oneNightKill, inline=True)

    oneNightReveal = '`[{}]`ON\n`[{}]`OFF' \
      .format(checkMark(self.oneNightReveal), 
              checkMark(not self.oneNightReveal))
    embed.add_field(name='[2]第1夜の占い', value=oneNightReveal, inline=True)

    discussTime = '{}分00秒'.format(self.discussTime)
    embed.add_field(name='話し合いの時間', value=discussTime, inline=True)

    jobNumList = self.jobManager.getJobDispList()
    embed.add_field(name="役職リスト", value=jobNumList, inline=True)
    
    joiners = self.playerManager.getPlayersListDisp()
    embed.add_field(name='参加者', value=joiners, inline=True)
    return embed
  
  def gamePlayerDisp(self):
    phaseColor = lambda phase: 0x7578bd if phase=='playing_night' else 0xfba779
    embed = discord.Embed(title='プレイヤーリスト', color=phaseColor(self.gameStateManager.nowState()))
    aliveList = self.playerManager.getAlivePlayerRolesListDisp()
    embed.add_field(name='生存者', value=aliveList, inline=True)
    deathList = self.playerManager.getDeathPlayerRolesListDisp()
    embed.add_field(name='死亡者', value=deathList, inline=True)
    return embed

  '''
  ゲームマスターのテキスト
  '''
  def comeNightText(self):
    title = '###{}日目の夜###'.format(self.dayCount)
    text = ''
    if self.dayCount == 1:
      text += 'みなさん、恐ろしい夜がやってきました\n'
    else:
      text += '容疑者を処刑したにもかかわらず、恐ろしい夜がまたやってきました\n'
    text += 'これから夜のアクションを行います\n' \
            'プライベートチャンネルでアクションを行ってください\n'
    embed = discord.Embed(title=title, description=text, color=0x7578bd)
    return embed
  
  def nextDay(self):
    self.gameStateManager.nextDay()
    self.dayCount += 1
    title = '###{}日目の朝###'.format(self.dayCoutnt)
    text = '夜が明けました\n昨夜処刑されたプレイヤーは\n'

  def requestNightActText(self):
    pass

  def requestVoteText(self):
    pass
