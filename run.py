from src.JinroClient import JinroClient

f = open('secret/.env')
env = f.read().split('\n')
f.close()

BOT_TOKEN = env[0]

client = JinroClient()
client.run(BOT_TOKEN)