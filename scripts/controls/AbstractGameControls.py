from abc import abstractmethod


class AbstractGameControls:
    def __init__(self):
        pass

    @abstractmethod
    def get_players_positions(self):
        pass
