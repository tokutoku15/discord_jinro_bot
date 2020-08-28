from src.job.Job import Job

class Villager(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('villager')
    super().setJobDispName('**村人**')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を人狼だと疑いました\n' \
            .format(target=targetId)
    return text

  def requestAct(self, emojiDict):
    emoji = emojiDict[self.jobName]
    emojiText = '<:{name}:{id}>'.format(name=emoji.name, id=emoji.id)
    text = 'あなたの役職は{job}{emoji}です\n' \
           '人狼だと疑うプレイヤーを選択してください\n' \
           '例: /act @player-ほげほげ\n' \
             .format(job=self.jobDispName, emoji=emojiText)
    return text