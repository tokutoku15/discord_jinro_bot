from src.job.Job import Job

class Fortuneteller(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('fortuneteller')
    super().setJobDispName('**占い師**')
    super().setWerewolf(False)
  
  def act(self, target, err=None):
    text = ''
    isHuman = lambda x: '人間' if x else '人狼'
    if not target.isAlive:
      text = '死亡者を選択するとはできません\n'
      err = 'error'
    else:
      text = '<@&{target}>を占いました\n' \
             '<@&{target}>は{isHuman}です\n' \
              .format(target=target.roleId, isHuman=isHuman(target.job.isWerewolf))
    return text, err

  def requestAct(self, emojiDict):
    emoji = emojiDict[self.jobName]
    emojiText = '<:{name}:{id}>'.format(name=emoji.name, id=emoji.id)
    text = 'あなたの役職は{job}{emoji}です\n' \
           '占うプレイヤー(生存者)を選択してください\n' \
             .format(job=self.jobDispName, emoji=emojiText)
    return text