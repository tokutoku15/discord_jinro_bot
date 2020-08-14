import discord
from time import sleep

from controller.PhaseController import PhaseController
from controller.phase import phase
from manager.GameMaster import GameMaster
from manager.PlayerManager import PlayerManager
from manager.RoleManager import RoleManager

class gameClient(discord.Client):

  def set_channel_id(self, channel_id):
    self.channel_id = channel_id

  async def on_ready(self):
    print('Logged in')
    print(self.user)
    print(self.user.id)
    print('---------')
    self.initialize()
  
  def check_channel_id(self, id):
    return id == self.channel_id

  async def on_message(self, message):
    if self.check_channel_id(message.channel.id):
      if self.user in message.mentions:
        if self.phaseController.getPhase() == phase[0]:
          self.phaseController.invitation()
          await self.proposal(message)
        else:
          await message.channel.send('ゲームはもう始まってます')

      if self.user != message.author:
        if self.phaseController.getPhase() == phase[1]:
          if message.content.startswith('参加'):
            await self.join(message)
          if message.content.startswith('確定'):
            self.phaseController.preparation()
            await self.decidePlayer(message)
            await self.waitRoleNum(message.channel)
        
        if self.phaseController.getPhase() == phase[2]:
          if '役職リスト' in message.content:
            await self.decideRole(message)
            self.roleManager.generateRoleStack()
            self.gameMaster = GameMaster(self.playerManager.getPlayerList(), self.roleManager.getRoleStack())
            await self.assignRole(message.channel)
    else:
      if self.user != message.author:
        await message.channel.send('人狼ゲームを始める時は{0}チャンネルでメンションしてね'.format(self.get_channel(self.channel_id)))
  

  async def proposal(self, message):
    rep = f'{message.author}から人狼ゲームの提案がされました\n'
    rep += 'ゲームに参加する人は「参加」と発言してください\n'
    await message.channel.send(rep)
    await self.join(message)
  
  async def join(self, message):
    self.playerManager.addPlayer(f'{message.author}', message.author.id)
    self.playerManager.decidePlayer()
    rep = f'{message.author}が参加しました\n'
    rep += '今の参加者は\n' + '-'*30 + '\n'
    rep += self.playerManager.getPlayersDisplay() + '\n'
    rep += '-'*30+'\nこのメンバーで開始するときは「確定」と発言してください'
    await message.channel.send(rep)
  
  async def decidePlayer(self, message):
    self.playerManager.decidePlayer()
    rep = 'このメンバーで確定しました\n' + '-'*30 + '\n'
    rep += self.playerManager.getPlayersDisplay() + '\n'
    rep += '-'*30+'\n'
    await message.channel.send(rep)

  async def waitRoleNum(self, channel):
    text = '次は役職の人数を決めます\n'
    text += '次のリストをコピペして人数を決めて送信してください\n'
    text += '{:-^30}\n'.format('役職リスト')
    text += self.roleManager.getRolesDisplay() + '\n'
    text += '-'*30 + '\n'
    await channel.send(text)
  
  async def decideRole(self, message):
    self.roleManager.updateRoleNum(message.content)
    rep = '役職を以下のように設定しました\n'
    rep += '{:-^30}\n'.format('役職リスト')
    rep += self.roleManager.getRolesDisplay() + '\n'
    rep += '-'*30 + '\n'
    await message.channel.send(rep)
  
  async def assignRole(self, channel):
    pay = 'あなたの役職は'
    for player in self.playerManager.getPlayerList():
      user = self.get_user(player.getUserId())
      await user.send(pay+player.WhoamI()+'です\n')
    text =  ''
    text += '役職を割り振りました\n'
    await channel.send(text)

  def initialize(self):
    self.phaseController = PhaseController()
    self.playerManager = PlayerManager()
    self.roleManager   = RoleManager()