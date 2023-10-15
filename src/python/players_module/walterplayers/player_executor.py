from os import getenv

import walterplayers


ia_flavour = getenv("WALTERONE_IA_FLAVOUR", "BipolarPlayer")
class_ = getattr(walterplayers, ia_flavour)


player = class_(0.5, 0.8)
player.run()
