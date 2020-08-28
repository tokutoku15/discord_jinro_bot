from src.job.Job import Job

class Werewolf(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('werewolf')
    super().setJobDispName('***人狼***')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を殺害対象に選択しました\n' \
            .format(target=targetId)
    return text
