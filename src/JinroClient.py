import discord
from src.manager.EmojiManager import EmojiManager
from src.manager.GameCommandManager import GameCommandManager

class JinroClient(discord.Client):

  '''
  discordにログインしたときに1度だけ実行
  '''
  async def on_ready(self):
    self.gameGuild = await self.creategameGuild("テストサーバ")
    self.gameChannel = await self.createJinroChannel("開発")
    self.emojiManger = EmojiManager()
    self.emojiManger.registerEmoji(self.gameGuild.emojis)
    await self.initialize()
    print(self.user.name)
    print(self.user.id)
    print('---------------')
    await self.gameChannel.send('Botのログインに成功！！')

  async def on_message(self, message):
    if self.user != message.author:
      print(message.content)
      await self.runCmd(message)
  
  async def runCmd(self, message):
    cmdResult, notification = self.gameCommandManager.parseMesAndRunCmd(message)
    if cmdResult is None:
      return
    else:
      if isinstance(cmdResult, str):
        await message.channel.send(cmdResult)
      elif isinstance(cmdResult, discord.Embed):
        await message.channel.send(embed=cmdResult)
      
      if notification == 'start':
        print('テキストチャンネル作成')
        await self.createAllPlayersChannel()
        await self.sendWerewolfChannel()
        await self.sendComeNightText()
      
      if notification == 'act':
        print('全員のアクションが終了')
        await self.gameChannel.send('全員のアクションが終了')

  '''
  ゲーム情報の初期化
  '''
  async def initialize(self):
    self.gameCommandManager = GameCommandManager(self.gameChannel)
    self.GM = self.gameCommandManager.GM
    await self.deleteChannel('人狼陣営')
    await self.deleteRole('player-')
  
  '''
  ゲームテキストの送信
  '''
  async def sendWerewolfChannel(self):
    await self.werewolfChannel.send(self.GM.werewolfChannelText())

  async def sendComeNightText(self):
    embed = self.GM.comeNightText()
    await self.gameChannel.send(embed=embed)
    for player in self.GM.playerManager.playerList.values():
      channel = player.myChannel
      job = player.job
      await channel.send(self.GM.requestNightActText(job, self.emojiManger.emojiIdDict))
      embed = self.GM.gamePlayerDisp()
      await channel.send(embed=embed)
  
  '''
  ギルド(サーバ)、チャンネル、ロールの管理
  '''
  async def creategameGuild(self, name):
    guild = discord.utils.get(self.guilds, name=name)
    return guild

  async def createJinroChannel(self, name):
    channel = discord.utils.get(self.gameGuild.channels, name=name)
    if channel is None:
      channel = await self.gameGuild.create_text_channel(name=name)
    return channel
  
  async def createAllPlayersChannel(self):
    werewolfs = []
    roles = []
    for userId, player in self.GM.playerManager.playerList.items():
      user = self.gameGuild.get_member(userId)
      guildRole = discord.utils.get(self.gameGuild.roles, name=player.discRoleName)
      if guildRole is None:
        guildRole = await self.gameGuild.create_role(name=player.discRoleName)
      userRole = discord.utils.get(user.roles, id=guildRole.id)
      if userRole is None:
        await user.add_roles(guildRole)
      roles.append(guildRole)
      if player.job.isWerewolf:
        werewolfs.append(guildRole)
      channel = discord.utils.get(self.gameGuild.channels, name=player.discRoleName)
      if channel is None:
        channel = await self.createPrivateChannel(roles, player.discRoleName)
      else:
        await channel.set_permissions(guildRole, read_messages=True)
      player.giveDiscRoleId(guildRole.id)
      player.giveChannel(channel)
      roles.clear()
    self.werewolfChannel = await self.createPrivateChannel(werewolfs, '人狼陣営')
  
  async def createPrivateChannel(self, playerRoles, channelName):
    botRole = discord.utils.get(self.gameGuild.roles, name="jinro_bot")
    overwrites = {
      self.gameGuild.default_role : discord.PermissionOverwrite(read_messages=False),
      botRole : discord.PermissionOverwrite(read_messages=True),
    }
    for role in playerRoles:
      overwrites[role] = discord.PermissionOverwrite(read_messages=True)
    channel = await self.gameGuild.create_text_channel(name=channelName, overwrites=overwrites)
    return channel
  
  async def deleteChannel(self, channelName):
    for channel in self.gameGuild.channels:
      if channel.name == channelName:
        await channel.delete()
  
  async def deleteRole(self, roleName):
    for role in self.gameGuild.roles:
      if roleName in role.name:
        await role.delete()