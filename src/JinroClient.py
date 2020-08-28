import discord
from src.manager.EmojiManager import EmojiManager
from src.manager.GameCommandManager import GameCommandManager

class JinroClient(discord.Client):

  '''
  discordにログインしたときに1度だけ実行
  '''
  async def on_ready(self):
    self.jinroGuild = await self.createJinroGuild("テストサーバ")
    self.jinroChannel = await self.createJinroChannel("開発")
    self.emojiManger = EmojiManager()
    self.emojiManger.registerEmoji(self.jinroGuild.emojis)
    self.initialize()
    print(self.user.name)
    print(self.user.id)
    print('---------------')
    await self.jinroChannel.send('Botのログインに成功！！')

  async def on_message(self, message):
    if self.user != message.author:
      print(message.content)
      await self.runCmd(message)
  
  async def runCmd(self, message):
    cmdResult = self.gameCommandManager.parseMesAndRunCmd(message)
    if cmdResult is None:
      return
    else:
      if isinstance(cmdResult, str):
        await self.jinroChannel.send(cmdResult)
      elif isinstance(cmdResult, discord.Embed):
        await self.jinroChannel.send(embed=cmdResult)

  '''
  ゲーム情報の初期化を行う
  '''
  def initialize(self):
    self.isSetupInfo = False
    self.gameCommandManager = GameCommandManager(self.jinroChannel)
  
  async def createJinroGuild(self, name):
    guild = discord.utils.get(self.guilds, name=name)
    return guild

  async def createJinroChannel(self, name):
    channel = discord.utils.get(self.jinroGuild.channels, name=name)
    if channel is None:
      channel = await self.jinroGuild.create_text_channel(name=name)
    return channel
  