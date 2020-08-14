from role.Role import Role

class Psychic(Role):

  def __init__(self):
    super().__init__()
    super().setDispName('霊媒師')
    super().setRole('psycic')
    super().setWerewolf(False) 