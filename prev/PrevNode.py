from abc import ABC, abstractmethod


class PrevNode(ABC):
    def __init__(self, node, align1, align2):
        self.node = node
        self.align1 = align1
        self.align2 = align2
        self.score = self.calc_score()
        self.priority = self.calc_priority()

    @abstractmethod
    def calc_score(self):
        pass

    @abstractmethod
    def calc_priority(self):
        pass
