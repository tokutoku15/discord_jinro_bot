import discord
from time import sleep

from controller.PhaseController import PhaseController
from controller.phase import phase
from controller.phase import gamePhase
from manager.GameMaster import GameMaster
from manager.GameLineManager import GameLineManager
from manager.PlayerManager import PlayerManager
from manager.RoleManager import RoleManager

class gameClient(discord.Client):

  def initialize(self):
    self.playerManager = PlayerManager()
    self.roleManager   = RoleManager()
    self.gameLineManager   = GameLineManager()
    self.commands = {
      '/act' : self.act,
      '/vote' : self.vote,
    }
    self.availableCommands = {
      'day' : ['/vote'],
      'night' : ['/act'],
    }
    '''アクションの受け付け'''
    self.isAcceptAct = False

  def set_text_channel_id(self, channel_id):
    self.channel_id = channel_id

  async def on_ready(self):
    print('Logged in')
    print(self.user)
    print(self.user.id)
    print('---------')
    self.initialize()
    self.jinroChannel = self.get_channel(self.channel_id)
    self.phaseController = PhaseController()
    await self.jinroChannel.send('Botのログインに成功しました')
  
  async def on_message(self, message):
    if self.user in message.mentions:
      if self.check_text_channel_id(message.channel.id):
        if self.phaseController.getPhase() == phase[0]:
          await self.proposalPhase(message)
        else:
          await message.channel.send('ゲームはもう始まってます')
      else:
        if self.user != message.author:
          await message.channel.send('人狼ゲームを始める時は{0}チャンネルでメンションしてね'.format(self.get_channel(self.channel_id)))
    else:
      if self.user != message.author:
        print(self.user)
        print(message.author)
        print()
        if self.check_text_channel_id(message.channel.id):
          if self.phaseController.getPhase() == phase[1]:
              await self.joinPhase(message)
              return
          if self.phaseController.getPhase() == phase[2]:
              await self.decideRolePhase(message)
              return
        elif self.check_dm_channel_id(message):
          if self.phaseController.getPhase() == phase[3]:
            await self.confirmPlayerRole(message)
            return
          if self.phaseController.getPhase() == gamePhase[0] \
            or self.phaseController.getPhase() == gamePhase[1]:
            await self.receiveAct(message)
            return
  
  def check_text_channel_id(self, id):
    return id == self.channel_id

  def check_dm_channel_id(self, message):
    if not self.playerManager.isUserIdInPlayerDict(message.author.id):
      return False
    dm = self.playerManager.getDMInfo(message.author.id)
    return dm.id == message.channel.id
  
  def acceptAct(self):
    self.isAcceptAct = True
  
  def dontAcceptAct(self):
    self.isAcceptAct = False
  
  def getIsAcceptAct(self):
    return self.isAcceptAct

  '''
  ゲーム開始のフェーズ
  '''
  async def proposalPhase(self, message):
    self.phaseController.invitation()
    await self.proposal(message)

  async def proposal(self, message):
    rep = self.gameLineManager.proposalLine(message.author)
    await message.channel.send(rep)
    await self.join(message)
  
  '''
  ゲーム参加者募集のフェーズ
  '''
  async def joinPhase(self, message):
    if message.content.startswith('参加'):
      await self.join(message)
    if message.content.startswith('確定'):
      self.phaseController.preparation()
      await self.decidePlayer(message)
      await self.sendRoleList(message.channel)
  
  async def join(self, message):
    self.playerManager.addPlayer(f'{message.author.display_name}', message.author.id)
    dm = await message.author.create_dm()
    self.playerManager.registerDM(message.author.id, dm)
    rep = self.gameLineManager.joinLine(message.author, self.playerManager.getPlayersDisplay())
    await message.channel.send(rep)
  
  async def decidePlayer(self, message):
    self.playerManager.updatePlayer()
    rep = self.gameLineManager.decidePlayerLine(
      self.playerManager.getPlayerNum(), 
      self.playerManager.getPlayersDisplaywithId()
    )
    await message.channel.send(rep)

  async def sendRoleList(self, channel):
    text = self.gameLineManager.requestRoleNumLine()
    await channel.send(text)
    text = self.gameLineManager.roleList(self.roleManager.getRolesDisplay())
    await channel.send(text)

  '''
  役職の人数決めフェーズ
  '''
  async def decideRolePhase(self, message):
    if '役職リスト' in message.content:
      if self.equalRoleNum(self.playerManager.getPlayerNum(), message.content):
        await self.decideRoleNum()
        await self.gameStart(message.channel)
      else:
        rep = self.gameLineManager.requestSendAgainLine()
        await message.channel.send(rep)
  
  def equalRoleNum(self, playerNum, content):
    return playerNum == self.roleManager.updateRoleNum(content)
  
  async def decideRoleNum(self):
    rep = self.gameLineManager.decideRoleNumLine(self.roleManager.getRolesDisplay())
    await self.jinroChannel.send(rep)
  
  async def assignRole(self, channel):
    isWerewolf = lambda x: '(人狼陣営):wolf:' if x else '(村人陣営):man:'
    sleep(3)
    for player in self.playerManager.getPlayerIdDict().values():
      user = self.get_user(player.getUserId())
      pay = self.gameLineManager.assignRoleLine(
        player.getRole().getDispName(), 
        isWerewolf(player.getRole().amIWerewolf()) )
      await user.send(pay)
    text = self.gameLineManager.finishSendRoleLine()
    await channel.send(text)
  
  async def gameStart(self, channel):
    self.roleManager.generateRoleStack()
    self.gameMaster = GameMaster(self.playerManager.getPlayerIdDict(), self.roleManager.getRoleStack())
    self.phaseController.playing()
    await self.assignRole(channel)
  
  '''
  ゲーム本編のフェーズ
  '''
  async def confirmPlayerRole(self, message):
    for player in self.playerManager.getPlayerIdDict().values():
      if message.author.id == player.getUserId():
        text = self.gameLineManager.confirmRoleLine(
                    message.author, 
                    player.gethasConfirmed())
        player.confirmRole()
        text += self.gameLineManager.confirmRoleLine2(self.playerManager.checkAllhasConfirmed())
        await message.channel.send(text)
        if self.playerManager.checkAllhasConfirmed():
          self.phaseController.nightCome()
          self.dontAcceptAct()
          await self.firstNightCome()
  
  '''夜のフェーズ'''
  async def firstNightCome(self):
    text = self.gameLineManager.gameStartLine()
    text += self.gameMaster.ruleDisp()
    text += self.gameMaster.nightCome()
    await self.jinroChannel.send(text)
    # sleep(2*60)
    await self.requestNightAct()
  
  async def nightPhase(self):
    text = self.gameMaster.nightCome()
    await self.jinroChannel.send(text)
    # sleep(2*60)
    await self.requestNightAct()
  
  async def requestNightAct(self):
    self.gameMaster.resetAllPlayerHasVoted()
    self.gameMaster.resetAllPlayerHasActed()
    actsDisp = self.availableCommands['night'][0]
    for player in self.playerManager.getPlayerIdDict().values():
      text = self.gameMaster.getDispDeadorAlive(player)
      text += self.gameMaster.nightAct(player, actsDisp)
      await player.getDM().send(text)
    self.acceptAct()
  
  '''昼のフェーズ'''
  async def dayPhase(self):
    text = self.gameMaster.sunRises()
    await self.jinroChannel.send(text)
    text = self.gameMaster.finishDiscussion()
    await self.jinroChannel.send(text)
    await self.requestDayVote()
  
  async def requestDayVote(self):
    actsDisp = self.availableCommands['day'][0]
    text = self.gameMaster.dayVote(actsDisp)
    self.gameMaster.resetAllPlayerHasVoted()
    for player in self.playerManager.getPlayerIdDict().values():
      await player.getDM().send(text)
    self.acceptAct()
  
  async def requestDayVoteAgain(self):
    text = self.gameMaster.dayVoteAgain()
    await self.jinroChannel.send(text)
    await self.requestDayVote()
  
  '''ゲームリザルトのフェーズ'''
  async def dispResult(self):
    serif, winner = self.gameMaster.isGameset()
    if winner != None: 
      self.phaseController.result()
      await self.sendGameResult(self.gameMaster.getDispResultPlayer(serif, winner))
      await self.resetAll()
    else:
      return

  async def resetAll(self):
    text = self.gameLineManager.gameEndLine()
    await self.jinroChannel.send(text)
    self.initialize()
    self.phaseController.pause()
  
  async def sendGameResult(self, resultText):
    self.phaseController.result()
    text = resultText
    await self.jinroChannel.send(text)

  '''アクションを受け取った時の処理'''
  async def receiveAct(self, message):
    if not self.getIsAcceptAct():
      return
    mes = message.content.split(' ')
    try:
      if mes[0] in self.availableCommands[self.phaseController.getPhase()]:
        commandResult = self.commands[mes[0]](mes[1:], message.author)
        await message.channel.send(commandResult)
    except KeyError:
      pass

    if self.gameMaster.checkAllPlayerHasActed():
      self.dontAcceptAct()
      if self.phaseController.getPhase() == gamePhase[0]:
        self.gameMaster.nightKill()
        await self.dispResult()
        if self.phaseController.getPhase() == phase[0]:
          return
        self.phaseController.sunRises()
        self.gameMaster.nextDay()
        await self.dayPhase()
        return
    if self.gameMaster.checkAllPlayerHasVoted():
      self.dontAcceptAct()
      if self.phaseController.getPhase() == gamePhase[1]:
        self.gameMaster.updateDispVotingTarget()
        if len(self.gameMaster.getVotingTarget()) > 1:
          await self.requestDayVoteAgain()
          return
        else:
          text = self.gameMaster.dayExecute()
          await self.jinroChannel.send(text)
          await self.dispResult()
          if self.phaseController.getPhase() == phase[0]:
            return
        await self.nightPhase()
        return

  def act(self, args, author):
    text = ''
    try:
      if len(args) > 1:
        text += '複数のプレイヤーを選択することはできません\n'
      elif len(args) < 1:
        text += '対象のプレイヤーを選択してください\n'
      else:
        targetId = int(args[-1])
        player = None
        for p in self.playerManager.getPlayerIdDict().values():
          if author.id == p.getUserId():
            player = p
        text += self.gameMaster.act(player, targetId)
    except ValueError:
      text += 'プレイヤーIDを指定してください\n'
    return text

  def vote(self, args, author):
    text = ''
    try:
      if len(args) > 1:
        text += '複数のプレイヤーを選択することはできません\n'
      elif len(args) < 1:
        text += '対象のプレイヤーを選択してください\n'
      else:
        targetId = int(args[-1])
        player = None
        for p in self.playerManager.getPlayerIdDict().values():
          if author.id == p.getUserId():
            player = p
        text += self.gameMaster.vote(player, targetId)
    except ValueError:
      text += 'プレイヤーIDを選択してください\n'
    return text
