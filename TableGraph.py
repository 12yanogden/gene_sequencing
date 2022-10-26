from Node import Node
from prev.enum.ScoreEnum import Score
from prev.UpperLeftNode import UpperLeftNode
from prev.UpperNode import UpperNode
from prev.LeftNode import LeftNode
from prev.enum.PriorityEnum import Priority


class TableGraph:
    def __init__(self, seq1, seq2, align_length):
        self.seq1 = "-" + seq1
        self.seq2 = "-" + seq2
        self.align_length1 = min(len(seq1) + 1, align_length + 1)
        self.align_length2 = min(len(seq2) + 1, align_length + 1)
        self.table_graph = []
        self.prevs = {}
        self.populate()

    def populate(self):
        for i in range(self.align_length1):
            self.table_graph.append([])
            self.prevs.append([])

            for j in range(self.align_length2):
                self.table_graph[i].append(None)
                self.prevs[i].append(None)

    def align_initial(self):
        initial_node = self.table_graph[0][0]
        initial_node[1] = ''
        initial_node[2] = ''
        initial_node[3] = 0

    def align_edges(self):
        for i in range(1, self.align_length1):
            curr = self.table_graph[i][0]
            curr[1] = self.seq1[i]
            curr[2] = '-'
            curr[3] = self.table_graph[i - 1][0][3] + Score.INS_DEL.value

        for j in range(1, self.align_length2):
            curr = self.table_graph[0][j]
            curr[1] = '-'
            curr[2] = self.seq2[j]
            curr[3] = self.table_graph[0][j - 1][3] + Score.INS_DEL.value

    def align(self):
        self.align_initial()
        self.align_edges()

        for i in range(1, self.align_length1):
            for j in range(1, self.align_length2):
                self.align_node(i, j)

    # ------------------------------------- Calc Prevs --------------------------------------#
    def calc_upper_left(self, i, j):
        return self.table_graph[i - 1][j - 1]

    def calc_upper(self, i, j):
        return self.table_graph[i - 1][j]

    def calc_left(self, i, j):
        return self.table_graph[i][j - 1]

    # ---------------------------------- Calc Prev Scores -----------------------------------#
    def calc_upper_left_score(self, upper_left, align1, align2):
        if align1 == align2:
            return upper_left[3] + Score.MATCH.value
        else:
            return upper_left[3] + Score.SUB.value

    # ------------------------------------ Calc Min Prev ------------------------------------#
    def calc_min_prev(self, i, j):
        upper_left = self.calc_upper_left(i, j)
        upper = self.calc_upper(i, j)
        left = self.calc_left(i, j)
        align1 = self.seq1[i]
        align2 = self.seq2[j]

        prevs = [[upper_left, self.calc_upper_left_score(upper_left, align1,  align2), Priority.UPPER_LEFT.value, align1, align2],
                 [upper, upper[3] + Score.INS_DEL.value, Priority.UPPER.value, align1, '-'],
                 [left, left[3] + Score.INS_DEL.value, Priority.LEFT.value, '-', align2]]
        min_prev = prevs[0]

        for prev in prevs:
            if prev[1] < min_prev[1] or\
                    (prev[1] == min_prev[1] and prev[2] < min_prev[2]):
                min_prev = prev

        return min_prev

    # ---------------------------------- Align Node[i][j] -----------------------------------#
    def align_node(self, i, j):
        curr = self.table_graph[i][j]
        prev = self.calc_min_prev(i, j)

        curr[0] = prev[0]
        curr[3] = prev[1]
        curr[1] = prev[3]
        curr[2] = prev[4]

    # ------------------------------------ Deliverables -------------------------------------#
    def get_last_node(self):
        return self.table_graph[self.align_length1 - 1][self.align_length2 - 1]

    def get_final_score(self):
        return self.get_last_node()[3]

    def get_alignments(self):
        alignments = ['', '']
        prev = self.get_last_node()

        while prev is not None:
            alignments[0] = prev[1] + alignments[0]
            alignments[1] = prev[2] + alignments[1]

            prev = prev[0]

        return alignments

    # ---------------------------------------- Debug ----------------------------------------#
    def to_string(self):
        out = ""

        # Print top row
        out += " \t"

        for j in range(self.align_length2):
            out += self.seq2[j] + "\t"

        out += "\n"

        # Print rest of table
        for i in range(self.align_length1):
            out += self.seq1[i] + "\t"

            for j in range(self.align_length2):
                out += str(self.table_graph[i][j][3]) + "\t"

            out += "\n"

        return out.expandtabs(8)

