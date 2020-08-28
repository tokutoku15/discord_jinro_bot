from abc import ABCMeta, abstractmethod

class Strategy(metaclass=ABCMeta):
  @abstractmethod
  def act(self):
    pass