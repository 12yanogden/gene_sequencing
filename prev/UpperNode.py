from prev.PrevNode import PrevNode
from prev.enum.ScoreEnum import Score
from prev.enum.PriorityEnum import Priority


class UpperNode(PrevNode):
    def __init__(self, node, align1, align2):
        super().__init__(node, align1, align2)

    def calc_score(self):
        return self.node.score + Score.INS_DEL.value

    def calc_priority(self):
        return Priority.UPPER.value
