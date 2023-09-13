
from drunk_player import DrunkPlayer
from billy_the_kid_player import BillyTheKidPlayer
from johnny_walker_player import JohnnyWalkerPlayer
from road_runner_player import RoadRunnerPlayer


life = 200
host = "http://127.0.0.1:8000"
username = "jmnieto"
password = "Gu4rma1986"
match = "2"

player = DrunkPlayer(life, host, username, password, match)
#player = BillyTheKidPlayer(life, host, username, password, match)
#player = JohnnyWalkerPlayer(life, host, username, password, match)
#player = RoadRunnerPlayer(life, host, username, password, match)


player.run()