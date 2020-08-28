from src.job.Job import Job

class Villager(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('villager')
    super().setJobDispName('***村人***')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を人狼だと疑いました\n' \
            .format(target=targetId)
    return text
