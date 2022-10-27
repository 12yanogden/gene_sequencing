from prev.PrevNode import PrevNode
from prev.enum.ScoreEnum import Score
from prev.enum.PriorityEnum import Priority


class UpperLeftNode(PrevNode):
    def __init__(self, node, align1, align2):
        super().__init__(node, align1, align2)

    def calc_score(self):
        if self.align1 == self.align2:
            return self.node.score + Score.MATCH.value
        else:
            return self.node.score + Score.SUB.value

    def calc_priority(self):
        return Priority.UPPER_LEFT.value
