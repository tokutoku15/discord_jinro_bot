from src.job.Job import Job

class Villager(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('villager')
    super().setJobDispName('**村人**')
    super().setWerewolf(False)
  
  def act(self, target, err=None):
    text = ''
    if not target.isAlive:
      text = '死亡者を選択することはできません\n'
      err = 'error'
    else:
      text = '<@&{target}>を人狼だと疑いました\n' \
              .format(target=target.roleId)
    return text, err

  def requestAct(self):
    emoji = self.emojiDict[self.jobName]
    text = 'あなたの役職は{job}{emoji}です\n' \
           '人狼だと疑うプレイヤーを選択してください\n' \
             .format(job=self.jobDispName, emoji=emoji)
    return text