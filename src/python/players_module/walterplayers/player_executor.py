#from os import getenv

#import walterplayers

#ia_flavour = getenv("WALTERONE_IA_FLAVOUR", "BipolarPlayer")
#class_ = getattr(walterplayers, ia_flavour)


#player = class_(0.5, 0.8)
#player.run()



from walterplayers.drunk_player import DrunkPlayer
from walterplayers.billy_the_kid_player import BillyTheKidPlayer
from walterplayers.johnny_walker_player import JohnnyWalkerPlayer
from walterplayers.road_runner_player import RoadRunnerPlayer
from walterplayers.bipolar.bipolar_player import BipolarPlayer

host = "localhost:8000"
password = "passwordmuysegura"
match = "2"



#player = DrunkPlayer(host, username, password, match)
#player = JohnnyWalkerPlayer(host, username, password, match)


road_runner_player = RoadRunnerPlayer(host, "RoadRunner", password, match)
#road_runner_player.run()


billy_the_kid_player = BillyTheKidPlayer(host, "BillyTheKid", password, match)
billy_the_kid_player.run()

drunk_player = DrunkPlayer(host, "Drunk", password, match)
#drunk_player.run()


johnny_player = JohnnyWalkerPlayer(host, "Johnny", password, match)
#johnny_player.run()

bipolar_player = BipolarPlayer(0.5, 0.8, host, "Bipolar", password, match)
#bipolar_player.run()

#player.run()