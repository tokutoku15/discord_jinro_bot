import discord

token_file = open('secret/.env')
JINRO_ENV = token_file.read().split('\n')
token_file.close()

DISCORD_BOT_TOKEN = JINRO_ENV[0]
JINRO_CHANNEL_ID  = int(JINRO_ENV[1])

client = discord.Client()

'''
人狼ゲームのフラグ管理
0...初期値/1...ゲーム参加者募集/2...役職決め/3〜5...ゲーム中のフラグ
'''
class GameFlagManager:
  def __init__(self):
    self.mode = 0
  def load_game_mode(self):
    return self.mode
  def set_game_mode(self, mode):
    self.mode = mode
  def invite_user_mode(self):
    self.set_game_mode(1)
  def decide_job_mode(self):
    self.set_game_mode(2)
  def finish_game(self):
    self.set_game_mode(0)


class GameController:

  def __init__(self, channel_id):
    self.channel_id = channel_id
    self.players = []
    self.jobs = {
      '村人(村人陣営)' : 0,
      '騎士(村人陣営)' : 0,
      '占い師(村人陣営)' : 0,
      '霊媒師(村人陣営)' : 0,
      '人狼(人狼陣営)' : 0,
    }

  def load_channel(self):
    print('channel is {}'.format(self.channel_id))
  
  def load_players(self):
    text = ''
    for player in self.players:
      text += str(player) + 'さん\n'
    return text
  
  def construct_jobs_text(self):
    text = '-'*30 + '\n'
    text += 'ここも含めてね\n'
    text += '-'*30 + '\n'
    for job in self.jobs:
      text += job + ':0人\n'
    text += '-'*30
    return text
  
  def parse_job_text(self, text):
    lines = text.split('\n')
    for line in lines:
      for job in self.jobs.keys():
        if job in line:
          self.jobs[job] = int(line.split(":")[1].split("人")[0])
    
  async def suggestion(self, message):
    self.players.append(f'{message.author}')
    rep = f'{message.author}さんから人狼ゲーム開始が提案されたよ\n'
    rep += 'ゲームに参加する人は「参加」と発言してね'
    await message.channel.send(rep)

  async def join(self, message):
    print(message.author)
    print(self.players)
    if str(message.author) in self.players:
      await message.channel.send(f'{message.author}さんはもう参加しているよ')
    else:
      self.players.append(f'{message.author}')
      rep = f'{message.author}さんが参加するよ\n'
      rep += f'ただいまの参加者 {len(self.players)}人\n{self.load_players()}'
      rep += 'プレイヤーが確定したら「確定」と発言してね'
      await message.channel.send(rep)

  async def wait_decide_job(self, message):
    rep = f'参加者は次の {len(self.players)}人で確定したよ\n'
    rep += f'{self.load_players()}\n'
    rep += '今からそれぞれの役職を決めるよ\n'
    rep += '下のテキストをコピペして人数を決めて送信してね\n'
    rep += self.construct_jobs_text()
    await message.channel.send(rep)
  
  async def decide_job(self, message):
    self.parse_job_text(message.content)
    rep = '役職の人数が決まったよ'
    rep += f'{self.jobs}'
    await message.channel.send(rep)
  
  async def job_text_send(self):
    for player in self.players:
      dm = await player.create_dm()
      await dm.send(f"あなたの役職は一般市民です")
  
  async def finish_game(self):
    self.players.clear()


class Player:
  def __init__(self, name):
    self.job = None 
    self.isSurvivor = True
    self.name = name
  def kill(self):
    self.isSurvivor = False
  def status(self):
    return [self.name, self.job, self.isSurvivor]


class Citizen(Player):
  def __init__(self, name):
    super().__init__(name)
    self.job = 'citizen'

gameFlagManager = GameFlagManager()
gameController  = GameController(JINRO_CHANNEL_ID)

citizen1 = Citizen('toku')
citizen2 = Citizen('kazu')
citizen2.kill()
print('citizen1\'s status is {}'.format(citizen1.status()))
print('citizen2\'s status is {}'.format(citizen2.status()))

'''Bot起動時に実行'''
@client.event
async def on_ready():
  print("Logged in as {0}".format(client.user))
  print('-'*30)


'''発言時に実行'''
@client.event
async def on_message(message):
  '''
  メンションされた時の処理
  とりあえずゲームを始めたい時のみメンションする
  '''
  if client.user in message.mentions: 
    if gameFlagManager.load_game_mode() == 0:
      if check_channel_id(message.channel.id):
          await gameController.suggestion(message)
          gameFlagManager.invite_user_mode()
      else:
        await message.channel.send('人狼ゲームを始める時は{0}チャンネルでメンションしてね！'.format(client.get_channel(JINRO_CHANNEL_ID)))
    else:
      await message.channel.send('今はゲームが始まってるよ')
  '''
  ゲームのプレイヤーを募集する時の処理
  「参加」を送信することで参加の確定
  '''
  if gameFlagManager.load_game_mode() == 1:
    if client.user != message.author:
      if message.content.startswith("参加"):
        await gameController.join(message)
      if message.content.startswith("確定"):
        await gameController.wait_decide_job(message)
        gameFlagManager.decide_job_mode()
  '''
  役職を決める時の処理
  TODO: 役職をアップデートして増やす
  '''
  if gameFlagManager.load_game_mode() == 2:
    if client.user != message.author:
      if 'ここも含めてね' in message.content:
        await gameController.decide_job(message)


def check_channel_id(chennel_id):
  return chennel_id == JINRO_CHANNEL_ID

client.run(DISCORD_BOT_TOKEN)