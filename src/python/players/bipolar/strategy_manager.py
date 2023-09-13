

class StrategyManager:
    ''' Manager of strategy. Given defensive and ofensive limit, a strategy will be choosen. '''


    def __init__(self, life_points, defensive_limit, offensive_limit):
        self._defensive_mode = False
        self._defenvise_mode_limit = defensive_limit * life_points
        self._offensive_mode_limit = offensive_limit * life_points
    
    def update_life_points(self, life_points):    
        if not self._defensive_mode and life_points <= self._defenvise_mode_limit:
            self._defensive_mode = True
            return

        if self._defensive_mode and self._life_points >= self._offensive_mode_limit:
            self._defensive_mode = False
            return

    def is_defensive_mode_active(self):
        return self._defensive_mode