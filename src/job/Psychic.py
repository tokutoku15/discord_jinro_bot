from src.job.Job import Job

class Psychic(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('psychic')
    super().setJobDispName('***霊媒師***')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を占いました\n' \
            .format(target=targetId)
    return text
