from role.Role import Role

class Villager(Role):

  def __init__(self):
    super().__init__()
    super().setDispName('村人')
    super().setRole('villager')
    super().setWerewolf(False)