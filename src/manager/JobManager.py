from src.job.Villager import Villager
from src.job.Werewolf import Werewolf
from src.job.Knight import Knight
from src.job.Psychic import Psychic
from src.job.Fortuneteller import Fortuneteller

class JobManager():
  
  def __init__(self):
    self.jobNumList = {
      Villager()      : 0,
      Werewolf()      : 0,
      Knight()        : 0,
      Psychic()       : 0,
      Fortuneteller() : 0,
    }
  
  def getJobDispList(self):
    text = '\n'.join([
      '[{jobId}]{jobName} : `{num}`人' \
        .format(jobId=jobId, jobName=job.jobDispName, num=self.jobNumList[job])
        for jobId, job in enumerate(list(self.jobNumList.keys()))
      ])
    return text
  
  def setJobNum(self, jobId, num):
    print(jobId)
    print(num)
    for i, job in enumerate(list(self.jobNumList.keys())):
      if jobId == i:
        self.jobNumList[job] = num