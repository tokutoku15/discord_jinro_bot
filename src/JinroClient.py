import discord

class JinroClient(discord.Client):

  async def on_ready(self):
    print(self.user.name)
    print(self.user.id)
    print('---------------')
    print(self.guilds)

  async def on_message(self, message):
    if self.user in message.mentions:
      if self.user != message.author:
        await self.presetDiscordInfo(message)
  
  async def presetDiscordInfo(self, message):
    self.jinroGuild = message.author.guild
    await self.createJinroChannel()
    await message.channel.send("セットアップが完了しました")
        
  async def createJinroChannel(self):
    channel = discord.utils.get(self.jinroGuild.channels, name="開発")
    print(channel)
    if channel is None:
      channel = await self.jinroGuild.create_text_channel(name="開発")
    self.jinroChannel = channel