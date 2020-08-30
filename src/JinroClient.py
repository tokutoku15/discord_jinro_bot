import discord
import asyncio
from src.manager.EmojiManager import EmojiManager
from src.manager.GameCommandManager import GameCommandManager

class JinroClient(discord.Client):

  '''
  discordにログインしたときに1度だけ実行
  '''
  async def on_ready(self):
    self.colorCode = {
      'player_role' : 0xe6e028
    }
    self.gameGuild = await self.createGameGuild("テストサーバ")
    self.gameChannel = await self.createJinroChannel("開発")
    self.emojiManger = EmojiManager()
    self.emojiManger.registerEmoji(self.gameGuild.emojis)
    self.gameCommandManager = GameCommandManager(self.gameChannel)
    self.GM = self.gameCommandManager.GM
    self.GM.jobManager.registerJobEmoji(self.emojiManger.emojiIdDict)
    await self.initialize()
    print(self.user.name)
    print(self.user.id)
    print('---------------')
    await self.gameChannel.send('Botがログインしました\nゲームを立ち上げる時は/setupコマンドを送信してください')
  
  async def initialize(self):
    await self.deleteChannel('人狼陣営')
    await self.deleteChannel('player-')
    await self.deleteRole('player-')

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
      
      if notification == 'setup':
        await self.initialize()
      
      if notification == 'start':
        print('テキストチャンネル作成')
        await self.createAllPlayersChannel()
        await self.sendWerewolfChannel()
        await self.gameChannel.send('それではゲームを始めます')
        await self.sendComeNightText()
      
      if notification == 'act':
        await self.sendNextDayText()
        isGameSet = await self.sendGameResult()
        if isGameSet:
          embed = self.GM.byeEmbed()
          await self.gameChannel.send(embed=embed)
          return
        await asyncio.sleep(3)
        # await self.displayRemainTime(self.GM.discussTime*60)
        await self.sendVoteTimeCome()
      
      if notification == 'vote':
        await self.sendVoteResult()
        if self.GM.gameStateManager.nowState() == 'playing_day':
          await self.sendVoteTargetList()
        elif self.GM.gameStateManager.nowState() == 'playing_night':
          isGameSet = await self.sendGameResult()
          if isGameSet:
            embed = self.GM.byeEmbed()
            await self.gameChannel.send(embed=embed)
            return
          await self.sendComeNightText()

  '''
  ゲームテキストの送信
  '''
  async def sendWerewolfChannel(self):
    await self.werewolfChannel.send(self.GM.werewolfChannelText())

  async def sendComeNightText(self):
    embed = self.GM.comeNightEmbed()
    # await asyncio.sleep(5)
    await self.gameChannel.send(embed=embed)
    # await asyncio.sleep(5)
    await self.sendActTargetList()
  
  async def sendActTargetList(self):
    for player in self.GM.playerManager.playerList.values():
      if player.isAlive:
        channel = player.myChannel
        job = player.job
        await channel.send(self.GM.requestNightActText(job, self.emojiManger.emojiIdDict))
        embed = self.GM.gamePlayersEmbed(player.job.jobName)
        await channel.send(embed=embed)
  
  async def sendNextDayText(self):
    await self.gameChannel.send('全員のアクションが終了しました')
    # await asyncio.sleep(5)
    embed = self.GM.nextDayEmbed()
    await self.gameChannel.send(embed=embed)

  async def sendVoteTimeCome(self):
    embed = self.GM.voteTimeComeEmbed()
    await self.gameChannel.send(embed=embed)
    # await asyncio.sleep(5)
    await self.sendVoteTargetList()

  async def sendVoteTargetList(self):
    text = self.GM.requestVoteText()
    embed = self.GM.voteTargetListEmbed()
    for player in self.GM.playerManager.playerList.values():
      if player.isAlive:
        channel = player.myChannel     
        await channel.send(text, embed=embed)
  
  async def sendVoteResult(self):
    await self.gameChannel.send('全員の投票が完了しました')
    # await asyncio.sleep(5)
    embed = self.GM.voteResultEmbed()
    await self.gameChannel.send(embed=embed)
  
  async def sendGameResult(self):
    embed = self.GM.gameSetEmbed(self.emojiManger.emojiIdDict)
    if embed is None:
      return False
    await self.gameChannel.send(embed=embed)
    return True
  
  '''
  ギルド(サーバ)、チャンネル、ロールの管理
  '''
  async def createGameGuild(self, name):
    guild = discord.utils.get(self.guilds, name=name)
    # if guild is None:
    #   guild = await self.create_guild(name=name)
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
        guildRole = await self.gameGuild.create_role(name=player.discRoleName, colour=discord.Colour(self.colorCode['player_role']))
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
      if channelName in channel.name:
        await channel.delete()
  
  async def deleteRole(self, roleName):
    for role in self.gameGuild.roles:
      if roleName in role.name:
        await role.delete()

  '''
  非同期を使って時間待機をするプログラム
  '''
  async def displayRemainTime(self, seconds):
    self.GM.startDiscussion()
    minute = seconds // 60
    second = seconds % 60
    text = '{:2d}分{:02d}秒'.format(minute, second)
    embed = discord.Embed(title='###話し合い時間###', description=text, colour=discord.Colour.dark_orange())
    mes = await self.gameChannel.send(embed = embed)
    while seconds > 0:
      seconds -= 1
      minute = seconds // 60
      second = seconds % 60
      text = '{:2d}分{:02d}秒'.format(minute, second)
      embed = discord.Embed(title='###話し合い時間###', description=text, colour=discord.Colour.dark_orange())
      await asyncio.sleep(0.9)
      await mes.edit(embed=embed)
    self.GM.finishDiscussion()