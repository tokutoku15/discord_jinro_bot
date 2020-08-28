from src.job.Job import Job

class Werewolf(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('werewolf')
    super().setJobDispName('**人狼**')
    super().setWerewolf(True)
  
  def act(self, targetId):
    text = '<@!{target}>を殺害対象に選択しました\n' \
            .format(target=targetId)
    return text
  
  def requestAct(self, emojiDict):
    emoji = emojiDict[self.jobName]
    emojiText = '<:{name}:{id}>'.format(name=emoji.name, id=emoji.id)
    text = 'あなたの役職は{job}{emoji}です\n' \
           '殺害するプレイヤーを選択してください\n' \
           '例: /act @player-ほげほげ\n' \
             .format(job=self.jobDispName, emoji=emojiText)
    return text