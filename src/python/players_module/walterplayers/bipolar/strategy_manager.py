from walterplayers.bipolar.constants import AdviserMode

class StrategyManager:
    ''' Manager of strategy. Given defensive and ofensive limit, a strategy will be choosen. '''

    def __init__(self, defensive_limit, offensive_limit):
        self._previous_adviser_mode = AdviserMode.Offensive
        self._adviser_mode = AdviserMode.Offensive
        self._defensive_limit = defensive_limit
        self._offensive_limit = offensive_limit
        self._defenvise_mode_limit = None
        self._offensive_mode_limit = None
        print('Strategy Manager created with Defensive Limit: ' +
            str(self._defensive_limit) + ' and Offensive Limit: ' +
            str(self._offensive_limit))

    def update_life_points(self, life_points):
        ''' Update life points to strategy manager. Life point is used to change strategy. '''
        if not self._defenvise_mode_limit or not self._offensive_mode_limit:
            #First time that the life points is updated, limits should be compute
            self._defenvise_mode_limit = self._defensive_limit * life_points
            self._offensive_mode_limit = self._offensive_limit * life_points
            print('Mode limits initialized with Deffensive Mode Limit : ' +
                str(self._defenvise_mode_limit) + ' and Offensive Mode Limit: ' +
                str(self._offensive_mode_limit))

        if (AdviserMode.Offensive == self._adviser_mode
            and life_points <= self._defenvise_mode_limit):
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.Defensive
            return

        if (AdviserMode.Defensive == self._adviser_mode
            and life_points >= self._offensive_mode_limit):
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.Offensive
            return

        self._previous_adviser_mode = self._adviser_mode

    def is_strategy_changed(self):
        ''' Return True if life point changes strategy to follow up. '''
        return self._previous_adviser_mode != self._adviser_mode

    def get_adviser_mode(self):
        ''' Return active adviser mode. '''
        return self._adviser_mode
