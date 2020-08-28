from src.job.Job import Job

class Knight(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('knight')
    super().setJobDispName('**騎士**')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を護衛します\n' \
            .format(target=targetId)
    return text

  def requestAct(self, emojiDict):
    emoji = emojiDict[self.jobName]
    emojiText = '<:{name}:{id}>'.format(name=emoji.name, id=emoji.id)
    text = 'あなたの役職は{job}{emoji}です\n' \
           '護衛するプレイヤーを選択してください\n' \
           '例: /act @player-ほげほげ\n' \
             .format(job=self.jobDispName, emoji=emojiText)
    return text