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
    self.initialize()
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
        await self.gameChannel.send(cmdResult)
      elif isinstance(cmdResult, discord.Embed):
        await self.gameChannel.send(embed=cmdResult)
      
      if notification == 'start':
        print('テキストチャンネル作成')
        await self.createAllPlayersChannel()

  '''
  ゲーム情報の初期化を行う
  '''
  def initialize(self):
    self.isSetupInfo = False
    self.gameCommandManager = GameCommandManager(self.gameChannel)
  
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
    for userId, player in self.gameCommandManager.GM.playerManager.playerList.items():
      roles = []
      user = self.gameGuild.get_member(userId)
      guildRole = discord.utils.get(self.gameGuild.roles, name=player.discRoleName)
      if guildRole is None:
        role = await self.gameGuild.create_role(name=player.discRoleName)
      userRole = discord.utils.get(user.roles, name=player.discRoleName)
      if userRole is None:
        await user.add_roles(role)
      if player.job.isWerewolf:
        werewolfs.append(role)
      channel = discord.utils.get(self.gameGuild.channels, name=player.discRoleName)
      if channel is not None:
        continue
      roles.append(role)
      channel = await self.createPrivateChannel(roles, player.discRoleName)
      player.giveChannel(channel)
    self.werewolfChannel = await self.createPrivateChannel(werewolfs, '人狼陣営')
  
  async def createPrivateChannel(self, roles, channelName):
    botRole = discord.utils.get(self.gameGuild.roles, name="jinro_bot")
    overwrites = {
      self.gameGuild.default_role : discord.PermissionOverwrite(read_messages=False),
      botRole : discord.PermissionOverwrite(read_messages=True),
    }
    for role in roles:
      overwrites[role] = discord.PermissionOverwrite(read_messages=True)
    channel = await self.gameGuild.create_text_channel(name=channelName, overwrites=overwrites)
    return channel