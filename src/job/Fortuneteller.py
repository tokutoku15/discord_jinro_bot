from src.job.Job import Job

class Fortuneteller(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('fortuneteller')
    super().setJobDispName('**占い師**')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を占いました\n' \
            .format(target=targetId)
    return text

  def requestAct(self, emojiDict):
    emoji = emojiDict[self.jobName]
    emojiText = '<:{name}:{id}>'.format(name=emoji.name, id=emoji.id)
    text = 'あなたの役職は{job}{emoji}です\n' \
           '占うプレイヤー(生存者)を選択してください\n' \
           '例: /act @player-ほげほげ\n' \
             .format(job=self.jobDispName, emoji=emojiText)
    return text