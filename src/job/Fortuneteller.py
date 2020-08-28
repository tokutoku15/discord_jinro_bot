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
