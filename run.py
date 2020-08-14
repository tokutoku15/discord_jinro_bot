from gameClient import gameClient

f = open('secret/.env')
env = f.read().split('\n')
f.close()

TOKEN = env[0]
CHANNEL_ID = int(env[1])

client = gameClient()
client.set_channel_id(CHANNEL_ID)
client.run(TOKEN)