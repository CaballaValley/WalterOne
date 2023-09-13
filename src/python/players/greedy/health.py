class Health:
    def __init__(self, life_points = 200):
        self._life_points = life_points
        self._defensive_mode = False
        self._defenvise_mode_limit = 0.8 * life_points
        self._ofensive_mode_limit = 0.9 * life_points
        
    def get_life_points(self):
        return self._life_points
    
    def update_life_points(self, life_points):
        self._life_points = life_points
        if self._life_points <= 0:
            print('I am died :(')
            return
        
        if not self._defensive_mode and self._life_points <= self._defenvise_mode_limit:
            self._defensive_mode = True
            print('Defensive mode active')
            return

        if self._defensive_mode and self._life_points >= self._ofensive_mode_limit:
            self._defensive_mode = False
            print('Ofensive mode active')
            return

    def is_defensive_mode_active(self):
        return self._defensive_mode
    
    def am_I_died(self):
        return self._life_points <= 0