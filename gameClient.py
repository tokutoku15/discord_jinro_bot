import discord
from time import sleep

from controller.PhaseController import PhaseController
from controller.phase import phase
from controller.phase import gamePhase
from manager.GameMaster import GameMaster
from manager.GameManager import GameManager
from manager.PlayerManager import PlayerManager
from manager.RoleManager import RoleManager

class gameClient(discord.Client):

  async def on_ready(self):
    print('Logged in')
    print(self.user)
    print(self.user.id)
    print('---------')
    self.jinroChannel = self.get_channel(self.channel_id)
    self.phaseController = PhaseController()
  
  async def on_message(self, message):
    if self.user in message.mentions:
      if self.check_channel_id(message.channel.id):
        if self.phaseController.getPhase() == phase[0]:
          await self.proposalPhase(message)
        else:
          await message.channel.send('ゲームはもう始まってます')
      else:
        if self.user != message.author:
          await message.channel.send('人狼ゲームを始める時は{0}チャンネルでメンションしてね'.format(self.get_channel(self.channel_id)))
    else:
      if self.user != message.author:
        if self.check_channel_id(message.channel.id):
          if self.phaseController.getPhase() == phase[1]:
            await self.joinPhase(message)
          if self.phaseController.getPhase() == phase[2]:
            await self.decideRolePhase(message)

  
  def set_channel_id(self, channel_id):
    self.channel_id = channel_id

  def check_channel_id(self, id):
    return id == self.channel_id

  '''
  ゲーム開始のフェーズ
  '''
  async def proposalPhase(self, message):
    self.initialize()
    await self.proposal(message)
    self.phaseController.invitation()

  async def proposal(self, message):
    rep = self.gameManager.proposalLine(message.author)
    await message.channel.send(rep)
    await self.join(message)
  
  '''
  ゲーム参加者募集のフェーズ
  '''
  async def joinPhase(self, message):
    if message.content.startswith('参加'):
      await self.join(message)
    if message.content.startswith('確定'):
      await self.decidePlayer(message)
      self.phaseController.preparation()
      await self.sendRoleList(message.channel)
  
  async def join(self, message):
    self.playerManager.addPlayer(f'{message.author}', message.author.id)
    self.playerManager.decidePlayer()
    rep = self.gameManager.joinLine(message.author, self.playerManager.getPlayersDisplay())
    await message.channel.send(rep)
  
  async def decidePlayer(self, message):
    self.playerManager.decidePlayer()
    rep = self.gameManager.decidePlayerLine(
      self.playerManager.getPlayerNum(), 
      self.playerManager.getPlayersDisplay()
    )
    await message.channel.send(rep)

  async def sendRoleList(self, channel):
    text = self.gameManager.roleListLine(self.roleManager.getRolesDisplay())
    await channel.send(text)

  '''
  役職の人数決めフェーズ
  '''
  async def decideRolePhase(self, message):
    if '役職リスト' in message.content:
      if self.equalRoleNum(self.playerManager.getPlayerNum(), message.content):
        await self.decideRoleNum(message.channel)
        self.roleManager.generateRoleStack()
        self.gameMaster = GameMaster(self.playerManager.getPlayerList(), self.roleManager.getRoleStack())
        self.phaseController.playing()
        await self.assignRole(message.channel)
      else:
        rep = self.gameManager.requestSendAgainLine()
        await message.channel.send(rep)
  
  def equalRoleNum(self, playerNum, content):
    return playerNum == self.roleManager.updateRoleNum(content)
  
  async def decideRoleNum(self, channel):
    rep = self.gameManager.decideRoleNumLine(self.roleManager.getRolesDisplay())
    await channel.send(rep)
  
  async def assignRole(self, channel):
    for player in self.playerManager.getPlayerList():
      isWerewolf = lambda x: '(人狼陣営):wolf:' if x else '(村人陣営):man:'
      user = self.get_user(player.getUserId())
      pay = self.gameManager.assignRoleLine(
        player.getRole().getDispName(), 
        isWerewolf(player.getRole().amIWerewolf()) )
      await user.send(pay)
    text = self.gameManager.finishSendRoleLine()
    await channel.send(text)

  def initialize(self):
    self.playerManager = PlayerManager()
    self.roleManager   = RoleManager()
    self.gameManager   = GameManager()