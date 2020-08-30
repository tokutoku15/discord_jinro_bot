from src.job.Job import Job

class Psychic(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('psychic')
    super().setJobDispName('**霊媒師**')
    super().setWerewolf(False)
  
  def act(self, target, err=None):
    text = ''
    if target.isAlive:
      text = '生存者を選択することはできません\n'
      err = 'error'
    else:
      text = '<@&{target}>を占いました\n' \
             '<@&{target}>は{isWerewolf}です\n' \
              .format(target=target.roleId, isWerewolf=target.job.isWerewolfWithEmoji())
    return text, err

  def requestAct(self):
    emoji = self.emojiDict[self.jobName]
    text = 'あなたの役職は{job}{emoji}です\n' \
           '占うするプレイヤー(死亡者)を選択してください\n' \
             .format(job=self.jobDispName, emoji=emoji)
    return text