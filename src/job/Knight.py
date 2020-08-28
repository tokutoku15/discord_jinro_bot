from src.job.Job import Job

class Knight(Job):

  def __init__(self):
    super().__init__()
    super().setJobName('knight')
    super().setJobDispName('**騎士**')
    super().setWerewolf(False)
  
  def act(self, targetId):
    text = '<@!{target}>を護衛します\n' \
            .format(target=targetId)
    return text
