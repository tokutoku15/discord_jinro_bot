from src.job.Job import Job

class Psychic(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('psychic')
    super().setJobDispName('**霊媒師**')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を占いました\n' \
            .format(target=targetId)
    return text

  def requestAct(self, emojiDict):
    emoji = emojiDict[self.jobName]
    emojiText = '<:{name}:{id}>'.format(name=emoji.name, id=emoji.id)
    text = 'あなたの役職は{job}{emoji}です\n' \
           '占うするプレイヤー(死亡者)を選択してください\n' \
           '例: /act @player-ほげほげ\n' \
             .format(job=self.jobDispName, emoji=emojiText)
    return text