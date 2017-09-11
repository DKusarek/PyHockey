from abc import abstractmethod


class AbstractGameControls:
    @abstractmethod
    def get_players_positions(self):
        pass
