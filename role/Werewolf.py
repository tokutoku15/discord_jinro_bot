from role.Role import Role

class Werewolf(Role):

  def __init__(self):
    super().__init__()
    super().setDispName('人狼')
    super().setRoleName('werewolf')
    super().setWerewolf(True) 