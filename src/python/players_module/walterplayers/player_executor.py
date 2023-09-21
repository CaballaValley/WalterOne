
from walterplayers.drunk_player import DrunkPlayer
from walterplayers.billy_the_kid_player import BillyTheKidPlayer
from walterplayers.johnny_walker_player import JohnnyWalkerPlayer
from walterplayers.road_runner_player import RoadRunnerPlayer


host = "http://127.0.0.1:8000"
username = "jmnieto"
password = "Gu4rma1986"
match = "2"

player = DrunkPlayer(host, username, password, match)
#player = BillyTheKidPlayer(host, username, password, match)
#player = JohnnyWalkerPlayer(host, username, password, match)
#player = RoadRunnerPlayer(host, username, password, match)


player.run()