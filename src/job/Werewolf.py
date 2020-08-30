from src.job.Job import Job

class Werewolf(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('werewolf')
    super().setJobDispName('**人狼**')
    super().setWerewolf(True)
  
  def act(self, target, err=None):
    text = ''
    if not target.isAlive:
      text = '死亡者を選択することはできません\n'
      err = 'error'
    else:
      text = '<@&{target}>を殺害対象に選択しました\n' \
              .format(target=target.roleId)
    return text, err
  
  def requestAct(self):
    emoji = self.emojiDict[self.jobName]
    text = 'あなたの役職は{job}{emoji}です\n' \
           '殺害するプレイヤーを選択してください\n' \
             .format(job=self.jobDispName, emoji=emoji)
    return text