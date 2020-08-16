from role.Role import Role

class Night(Role):

  def __init__(self):
    super().__init__()
    super().setDispName('騎士')
    super().setRoleName('night')
    super().setWerewolf(False)