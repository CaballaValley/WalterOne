
class Adviser():
    def add_or_update_zone(self, find_response):
        ''' Method to update zone information into an adviser. '''
        pass

    def remove_zone(self, zone):
        ''' A zone cuold be remove and this must be notify to an adviser'''
        pass

    def reset_strategy(self):
        ''' Reset strategy! Change defensive <-> offensive'''
        pass
    
    def get_next_action(self, find_response):
        ''' Method to compute next action following a strategy by an adviser. '''
        pass
