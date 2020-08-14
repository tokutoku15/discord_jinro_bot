from role.Role import Role

class FortuneTeller(Role):

  def __init__(self):
    super().__init__()
    super().setDispName('占い師')
    super().setRole('fortuneteller')
    super().setWerewolf(False)