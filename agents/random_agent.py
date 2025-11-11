import numpy as np
from agents.agent import Agent

class RandomAgent(Agent):
    def __init__(self):
        pass

    def act(self, obs, legal_moves):
        """
        Acts randomly.
        """
        legal_move_list = np.where(legal_moves)[0]
        action = np.random.choice(legal_move_list)
        return int(action), self