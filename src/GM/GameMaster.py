import random
import discord
from src.manager.PlayerManager import PlayerManager
from src.manager.GameStateManager import GameStateManager
from src.manager.JobManager import JobManager

class GameMaster():

  def __init__(self, gameChannel):
    self.gameChannel = gameChannel
    self.jobManager = JobManager()
    self.colorCode = {
      'other' : 0x09d73d,
      'playing_night' : 0x7578bd,
      'playing_day' : 0x40e7e5,
      'playing_vote' : 0xff9900
    }
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
      'playing_discuss' : {
        'display' : '話し合い中',
        'commands' : {},
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
          '/help':'利用可能なコマンドの確認',
          '/stopbot' : 'ゲームの中断とBotの停止'
        }
      },
    }
    self.initialize()

  def initialize(self):
    self.dayCount = 1
    self.discussTime = 5
    self.gameStateManager = GameStateManager()
    self.playerManager = PlayerManager()
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
      return None, None
    if self.gameStateManager.nowState() != 'pause':
      err = self.getPhaseText() + '/setupコマンドは使用できません'
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
    ret = self.gameOptEmbed(description=description)
    return ret, 'setup'
  
  '''joinコマンド'''
  def join(self, message):
    if self.gameChannel != message.channel:
      return None, None
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseText()+'/joinコマンドは使用できません'
      return err, 'error'
    author = message.author
    self.playerManager.addPlayer(author.display_name, author.id)
    description = "<@!{userId}>がゲームに参加しました" \
                      .format(userId=author.id)
    ret = self.gameOptEmbed(description=description)
    return ret, 'join'
  
  '''exitコマンド'''
  def exit(self, message):
    if self.gameChannel != message.channel:
      return None, None
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseText()+'/exitコマンドは使用できません'
      return err, 'error'
    author = message.author
    self.playerManager.removePlayer(author.id)
    description = "<@!{userId}>がゲームから退出しました" \
                    .format(userId=author.id)
    ret = self.gameOptEmbed(description=description)
    return ret, 'exit'
  
  '''optionコマンド'''
  def option(self, message):
    if self.gameChannel != message.channel:
      return None, None
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseText()+'/optionコマンドは使用できません'
      return err, 'error'
    mes = message.content.split(' ')
    err = '対象のオプションIDまたはオプションが認識できません\n' \
          '/set [対象のオプションID] [on/off] でルールを設定してください\n' \
          '例: 第一夜の殺害をONにする場合\n' \
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
    ret = self.gameOptEmbed()
    return ret, 'option'
  
  '''timeコマンド'''
  def time(self, message):
    if self.gameChannel != message.channel:
      return None, None
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseText()+'/timeコマンドは使用できません'
      return err, 'error'
    mes = message.content.split(' ')
    err = '時間を正しく設定できていません\n' \
          '/time [時間(分)] で話し合いの時間を設定してください(最大20分、最小1分)\n' \
          '例: 話し合いの時間を3分にする場合\n' \
          '**/time 3**'
    try:
      if len(mes) != 2:
        return err, 'error'
      setTime = int(mes[1])
      if setTime <= 0 or 20 <= setTime:
        return err, 'error'
    except ValueError:
      return err, 'error'
    self.discussTime = setTime
    embed = self.gameOptEmbed()
    return embed, 'time'
  
  '''jobコマンド'''
  def job(self, message):
    if self.gameChannel != message.channel:
      return None, None
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseText()+'/jobコマンドは使用できません'
      return err, 'error'
    mes = message.content.split(' ')
    index = 1
    err = '対象の役職IDが認識できません\n' \
          '/job [対象の役職ID] [人数]... で役職の人数を設定してください\n' \
          '複数の役職の人数も設定できます\n' \
          '例: 村人を3人、人狼を2人に設定する場合\n' \
          '**/job 0 3 1 2**' 
    if len(mes[index:]) < 2:
      return err, 'error'
    try:
      while len(mes[index:]) >= 2:
        jobId = int(mes[index])
        jobNum = int(mes[index+1])
        if jobId >= len(self.jobManager.jobNumList):
          return err, 'error'
        self.jobManager.setJobNum(jobId, jobNum)
        index += 2
    except ValueError:
      return err, 'error'
    ret = self.gameOptEmbed()
    return ret, 'job'
  
  '''startコマンド'''
  def start(self, message):
    if self.gameChannel != message.channel:
      return None, None
    if self.gameStateManager.nowState() != 'setup':
      err = self.getPhaseText()+'/startコマンドは使用できません'
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

  '''actコマンド'''
  def act(self, message):
    if not self.isFromPlayersChannel(message):
      return None, None
    if self.gameStateManager.nowState() != 'playing_night':
      err = self.getPhaseText()+'/actコマンドは使用できません'
      return err, 'error'
    author = self.playerManager.playerList[message.author.id]
    if author.hasActed:
      err = 'もうアクションは終えています\n他のプレイヤーのアクションが終わるまでしばらくお待ちください\n'
      return err, 'error'
    mes = message.content.split(' ')
    if len(mes) > 2:
      err = '対象が多すぎます\n1人だけ選択してください\n'
      return err, 'error'
    if not '<@&' in mes[1]:
      err = '対象プレイヤーを認識できません\n'
      return err, 'error'
    targetRoleId = int(mes[1].lstrip('<@&').rstrip('>'))
    authorRoleId = author.roleId
    if targetRoleId == authorRoleId:
      err = '自分を対象に選択することはできません\n他のプレイヤーを選んでください\n'
      return err, 'error'
    ret, err = self.jobAct(targetRoleId, message.author)
    if not err is None:
      return ret, err
    else:
      if not self.playerManager.allPlayerHasActed():
        return ret, None
    self.gameStateManager.daytime()
    return ret, 'act'
  
  '''voteコマンド'''
  def vote(self, message):
    if not self.isFromPlayersChannel(message):
      return None, None
    if self.gameStateManager.nowState() != 'playing_day':
      err = self.getPhaseText()+'/voteコマンドは使用できません'
      return err, 'error'
    author = self.playerManager.playerList[message.author.id]
    if author.hasVoted:
      err = 'もう投票は終えています\n他のプレイヤーの投票が終わるまでしばらくお待ちください\n'
      return err, 'error'
    mes = message.content.split(' ')
    if len(mes) > 2:
      err = '対象が多すぎます\n1人だけ選択してください\n'
      return err, 'error'
    if not '<@&' in mes[1]:
      err = '対象プレイヤーを認識できません\n'
      return err, 'error'
    targetRoleId = int(mes[1].lstrip('<@&').rstrip('>'))
    authorRoleId = author.roleId
    if targetRoleId == authorRoleId:
      err = '自分を対象に選択することはできません\n他のプレイヤーを選んでください\n'
      return err, 'error'
    ret, err = self.dayVote(targetRoleId, message.author)
    if not err is None:
      return ret, err
    else:
      if not self.playerManager.allPlayerHasVoted():
        return ret, None
    return ret, 'vote'
    
  '''helpコマンド'''
  def help(self, message):
    if self.gameChannel != message.channel:
      if 'playing' in self.gameStateManager.nowState():
        if not self.isFromPlayersChannel(message):
          return None, 'error'
      else:
        return None, 'error'
    embed = self.commandsEmbed()
    return embed, 'help'

  '''
  ユーティリティ関数
  '''
  def isFromPlayersChannel(self, message):
    try:
      mesChnId = message.channel.id
      playerChnId = self.playerManager.playerList[message.author.id].myChannel.id
      return mesChnId == playerChnId
    except KeyError:
      return False

  def giveRoleAndJob(self):
    jobs = self.jobManager.getJobStack()
    for player in self.playerManager.playerList.values():
      roleName = 'player-{}'.format(player.name)
      random.shuffle(jobs)
      player.giveDiscRole(roleName)
      player.giveJob(jobs.pop(0))

  def jobAct(self, targetRoleId, author, ret=None, err=None):
    author = self.playerManager.playerList[author.id]
    authorJob = author.job
    targetPlayer = None
    for player in self.playerManager.playerList.values():
      if targetRoleId == player.roleId:
        targetPlayer = player
        break
    if authorJob.jobName == 'werewolf':
      if self.dayCount == 1 and not self.oneNightKill:
        ret, err = author.vote(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.voteMe()
      else:
        ret, err = authorJob.act(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.willKill()
    elif authorJob.jobName == 'fortuneteller':
      if self.dayCount == 1 and not self.oneNightReveal:
        ret, err = author.vote(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.voteMe()
      else:
        ret, err = authorJob.act(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.revealMe()
    elif authorJob.jobName == 'psychic':
      if self.dayCount == 1:
        ret, err = author.vote(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.voteMe()
      else:
        ret, err = authorJob.act(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.deathRevealMe()
    elif authorJob.jobName == 'knight':
      if self.dayCount == 1 and not self.oneNightKill:
        ret, err = author.vote(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.voteMe()
      else:
        ret, err = authorJob.act(targetPlayer)
        if not err is None:
          return ret, err
        targetPlayer.protectMe()
    else:
      ret, err = authorJob.act(targetPlayer)
      if not err is None:
        return ret, err
      targetPlayer.voteMe()
    author.finishAct()
    return ret, err

  def nightActResult(self):
    killPlayerId = None
    maxVote = 0
    doubtPlayers = []
    for userId, player in self.playerManager.playerList.items():
      if player.willBeKilled and not player.isProtected:
        if killPlayerId is None:
          killPlayerId = userId
          player.killMe()
      if player.isAlive:
        if maxVote < player.votedCount:
          doubtPlayers.clear()
          maxVote = player.votedCount
          doubtPlayers.append(userId)
        elif maxVote == player.votedCount:
          doubtPlayers.append(userId)
      player.nextDay()
    killPlayerText = '<@!{}>'.format(killPlayerId)
    doubtPlayersIdList = '>\n<@!'.join([
      str(userId) for userId in doubtPlayers
    ])
    doubtPlayersText = '<@!{}>\n'.format(doubtPlayersIdList)
    if killPlayerId is None:
      killPlayerText = None
    self.playerManager.resetAllPlayerHasActed()
    return killPlayerText, doubtPlayersText

  def dayVote(self, targetRoleId, author, ret=None, err=None):
    author = self.playerManager.playerList[author.id]
    targetPlayer = None
    for player in self.playerManager.playerList.values():
      if targetRoleId == player.roleId:
        ret, err = author.vote(player)
        if not err is None:
          return err, err
        player.voteMe()
        author.finishVote()
    return ret, err

  def getPhaseText(self):
    phase = self.gameStateManager.nowState()
    phaseText = self.stateDisp[phase]['display']
    text = '今のフェーズは{phase}です\n'.format(phase=phaseText)
    return text

  def gameOptEmbed(self, **kwargs):
    description = None
    if 'description' in kwargs.keys():
      description = kwargs['description']
    embed = discord.Embed(title='Jinro Bot', description=description, colour=self.colorCode['other'])

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
  
  def gamePlayersEmbed(self, jobName):
    embed = discord.Embed(title='プレイヤーリスト', colour=self.colorCode[self.gameStateManager.nowState()])
    aliveList = self.playerManager.getAlivePlayerRolesListDisp(jobName)
    embed.add_field(name='生存者', value=aliveList, inline=True)
    deathList = self.playerManager.getDeathPlayerRolesListDisp(jobName)
    embed.add_field(name='死亡者', value=deathList, inline=True)
    return embed
  
  def commandsEmbed(self):
    embed = discord.Embed(title="Help", description="利用できるコマンドは以下の通りです", colour=self.colorCode['other'])
    for phase in self.stateDisp.keys():
      text = ''
      if len(self.stateDisp[phase]['commands']) != 0:
        text = '\n'.join([
          '{cmd} : {description}'.format(cmd=cmd, description=description)
          for cmd, description in self.stateDisp[phase]['commands'].items()
        ])
        embed.add_field(name=self.stateDisp[phase]['display'], value=text, inline=False)
    return embed

  def startDiscussion(self):
    self.gameStateManager.discussion()
  
  def finishDiscussion(self):
    self.gameStateManager.daytime() 
  
  def isGameSet(self):
    winner = None
    aliveWerewolf = [
      player for player in self.playerManager.playerList.values()
      if player.isAlive and player.job.isWerewolf
    ]
    aliveVillager = [
      player for player in self.playerManager.playerList.values()
      if player.isAlive and not player.job.isWerewolf
    ]
    if len(aliveWerewolf) == 0:
      winner = 'villager'
    elif len(aliveWerewolf) >= len(aliveVillager):
      winner = 'werewolf'
    if not winner is None:
      self.gameStateManager.gameResult()
    return winner

  '''
  ゲームマスターのセリフテキスト
  '''
  def werewolfChannelText(self):
    text = 'ここは人狼陣営専用のテキストチャンネルです\n' \
          '誰を襲撃するかなどを相談するチャットスペースとして利用できます\n'
    return text

  def comeNightEmbed(self):
    title = '###{}日目の夜###'.format(self.dayCount)
    text = ''
    if self.dayCount == 1:
      text += 'みなさん、恐ろしい夜がやってきました\n'
    else:
      text += '容疑者を処刑したにもかかわらず、恐ろしい夜がまたやってきました\n'
    text += 'これから夜のアクションを行います\n' \
            'プライベートチャンネルでアクションを行ってください\n'
    embed = discord.Embed(title=title, description=text, colour=self.colorCode[self.gameStateManager.nowState()])
    return embed
  
  def nextDayEmbed(self):
    self.dayCount += 1
    killedPlayer, doubtPlayers = self.nightActResult()
    title = '###{}日目の朝###'.format(self.dayCount)
    text = '夜が明けました\n昨晩襲撃されたプレイヤーは\n'
    if killedPlayer is None:
      text += 'いませんでした\n'
    else:
      text += '{killPlayer}です\n'.format(killPlayer=killedPlayer)
    text += 'そして人狼と疑われているプレイヤーは\n' \
            '{doubtPlayers}です\nこれから人狼を探すために話し合ってください\n' \
            '話し合いの時間は今から{time}分です\n' \
             .format(doubtPlayers=doubtPlayers, time=self.discussTime)
    embed = discord.Embed(title=title, description=text, colour=self.colorCode[self.gameStateManager.nowState()])
    return embed

  def voteResultEmbed(self):
    maxVote = 0
    self.execution = []
    for userId, player in self.playerManager.playerList.items():
      if maxVote < player.votedCount:
        self.execution.clear() 
        maxVote = player.votedCount
        self.execution.append((userId, player))
      elif maxVote == player.votedCount:
        self.execution.append((userId, player))
      player.resetCount()
    if len(self.execution) > 1:
      title = '###決選投票###'
      executionText = '>\n<@!'.join([
        str(userId) for userId, execution in self.execution
      ])
      text = '投票の結果、最多票が複数名いました\n' \
            '<@!{}>\nです\n決選投票を行うのでプライベートチャンネルで投票を行ってください' \
              .format(executionText)
      embed = discord.Embed(title=title, description=text, colour=discord.Colour.dark_orange())
      self.playerManager.resetAllPlayerHasVoted()
      return embed
    else:
      self.playerManager.playerList[self.execution[-1][0]].killMe()
      title = '###処刑実行###'
      text = '投票の結果、処刑されるプレイヤーは\n' \
             '<@!{execution}>\nです\n<@!{execution}>はこのゲームが終わるまでゲームの内容について話すことはできません\n' \
               .format(execution=self.execution[-1][0])
      embed = discord.Embed(title=title, description=text, colour=discord.Color.dark_orange())
      self.gameStateManager.nightCome()
      return embed
        

  def voteTimeComeEmbed(self):
    title = '###投票の時間###'
    text = '話し合いは終了です\nここからはゲームの内容について話してはいけません\n' \
           '今から処刑するプレイヤーを決めるため投票を行います\n' \
           'プライベートチャンネルで投票を行ってください\n'
    embed = discord.Embed(title=title, description=text, colour=discord.Colour.dark_orange())
    return embed

  def requestNightActText(self, job, emojiDict):
    text = job.requestAct()
    text += '例: 「@player-ほげほげ」に対してアクションを行う場合\n**/act @player-ほげほげ**\n'
    if self.dayCount == 1:
      if job.jobName == 'werewolf':
        if not self.oneNightKill:
          text += '※ 第一夜の殺害はできません\n'
      elif job.jobName == 'fortuneteller':
        if not self.oneNightReveal:
          text += '第一夜での占いはできないので人狼だと疑うプレイヤーを選択してください\n'
      elif job.jobName == 'psychic':
        text += '死亡者がいないので人狼だと疑うプレイヤーを選択してください\n'
      elif job.jobName == 'knight':
        if not self.oneNightKill:
          text += '第一夜の殺害は「なし」なので人狼だと疑うプレイヤーを選択してください\n'
    return text

  def requestVoteText(self):
    text = '処刑するプレイヤーに投票してください\n' \
           '例: 「@player-ほげほげ」に投票する場合\n**/vote @player-ほげほげ**'
    return text 
  
  def voteTargetListEmbed(self):
    targetListText = ''
    if hasattr(self, 'execution'):
      if len(self.execution) > 1:
        targetList = '>\n<@&'.join([
          str(player.roleId) for _, player in self.execution
        ])
        targetListText = '<@&{}>'.format(targetList)
      else:
        targetListText = self.playerManager.getAlivePlayerRolesListDisp()
    else:
      targetListText = self.playerManager.getAlivePlayerRolesListDisp()
    embed = discord.Embed(title='プレイヤーリスト', description=targetListText, colour=discord.Colour.dark_orange())
    return embed

  def gameSetEmbed(self, emojiDict):
    ret = self.isGameSet()
    if ret is None:
      return None
    embed = None
    alive = lambda x: '生存' if x else '死亡'
    werewolf = [
      '<@!{userId}> [{jobName}] ({alive})' \
        .format(userId=userId, jobName=player.job.getJobNameWithEmoji(), alive=alive(player.isAlive))
      for userId, player in self.playerManager.playerList.items()
      if player.job.isWerewolf
    ]
    villager = [
      '<@!{userId}> [{jobName}] ({alive})' \
        .format(userId=userId, jobName=player.job.getJobNameWithEmoji(), alive=alive(player.isAlive))
      for userId, player in self.playerManager.playerList.items()
      if not player.job.isWerewolf
    ]
    werewolfText = '\n'.join(werewolf)
    villagerText = '\n'.join(villager)
    url = "https://cdn.discordapp.com/emojis/{emojiid}" \
            .format(emojiid=emojiDict[ret].id)
    if ret == 'villager':
      embed = discord.Embed(title='村人の勝利！', color=0x0)
      embed.set_thumbnail(url=url)
      embed.add_field(name="勝者", value=villagerText, inline=True)
      embed.add_field(name="敗者", value=werewolfText, inline=True)
    elif ret == 'werewolf':
      embed = discord.Embed(title='人狼の勝利！', color=0xffffff)
      embed.set_thumbnail(url=url)
      embed.add_field(name="勝者", value=werewolfText, inline=True)
      embed.add_field(name="敗者", value=villagerText, inline=True)
    return embed

