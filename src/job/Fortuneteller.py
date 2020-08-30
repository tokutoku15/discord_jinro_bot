from src.job.Job import Job

class Fortuneteller(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('fortuneteller')
    super().setJobDispName('**占い師**')
    super().setWerewolf(False)
  
  def act(self, target, err=None):
    text = ''
    if not target.isAlive:
      text = '死亡者を選択するとはできません\n'
      err = 'error'
    else:
      text = '<@&{target}>を占いました\n' \
             '<@&{target}>は{isWerewolf}です\n' \
              .format(target=target.roleId, isWerewolf=target.job.isWerewolfWithEmoji())
    return text, err

  def requestAct(self):
    emoji = self.emojiDict[self.jobName]
    text = 'あなたの役職は{job}{emoji}です\n' \
           '占うプレイヤー(生存者)を選択してください\n' \
             .format(job=self.jobDispName, emoji=emoji)
    return text