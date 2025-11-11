from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def act(self, obs, legal_moves):
        pass