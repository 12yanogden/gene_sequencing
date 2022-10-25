from Node import Node
from prev.enum.ScoreEnum import Score
from prev.UpperLeftNode import UpperLeftNode
from prev.UpperNode import UpperNode
from prev.LeftNode import LeftNode


class TableGraph:
    def __init__(self, seq1, seq2, align_length):
        self.seq1 = "-" + seq1
        self.seq2 = "-" + seq2
        self.align_length1 = min(len(seq1) + 1, align_length + 1)
        self.align_length2 = min(len(seq2) + 1, align_length + 1)
        self.table_graph = []
        self.populate_table_graph()

    def populate_table_graph(self):
        for i in range(self.align_length1):
            self.table_graph.append([])

            for j in range(self.align_length2):
                self.table_graph[i].append(Node(i, j))

    def align_edges(self):
        self.table_graph[0][0].score = 0
        self.table_graph[0][0].align1 = ''
        self.table_graph[0][0].align2 = ''

        for i in range(1, self.align_length1):
            curr = self.table_graph[i][0]
            curr.score = self.table_graph[i - 1][0].score + Score.INS_DEL.value
            curr.align1 = self.seq1[i]
            curr.align2 = '-'

        for j in range(1, self.align_length2):
            curr = self.table_graph[0][j]
            curr.score = self.table_graph[0][j - 1].score + Score.INS_DEL.value
            curr.align1 = '-'
            curr.align2 = self.seq2[j]

    def align(self):
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
    def calc_upper_left_score(self, upper_left):
        if self.seq1[upper_left.i] == self.seq2[upper_left.j]:
            return upper_left.score + Score.MATCH
        else:
            return upper_left.score + Score.SUB.value

    def calc_upper_score(self, upper):
        return upper.score + Score.INS_DEL.value

    def calc_left_score(self, left):
        return left.score + Score.INS_DEL.value

    # ------------------------------------ Calc Min Prev ------------------------------------#
    def calc_prevs(self, i, j):
        align1 = self.seq1[i]
        align2 = self.seq2[j]
        prevs = []

        left = self.calc_left(i, j)
        upper = self.calc_upper(i, j)
        upper_left = self.calc_upper_left(i, j)

        prevs.append(LeftNode(left, '-', align2))
        prevs.append(UpperNode(upper, align1, '-'))
        prevs.append(UpperLeftNode(upper_left, align1, align2, self.seq1[i], self.seq2[j]))

        return prevs

    def calc_min_prev(self, i, j):
        prevs = self.calc_prevs(i, j)
        min_prev = prevs[0]

        for prev in prevs:
            if prev.score < min_prev.score:
                min_prev = prev
            elif prev.score == min_prev.score and prev.priority < min_prev.priority:
                min_prev = prev

        return min_prev

    # ---------------------------------- Align Node[i][j] -----------------------------------#
    def align_node(self, i, j):
        # print("i:", i)
        # print("j:", j)
        # print()
        curr = self.table_graph[i][j]
        prev = self.calc_min_prev(i, j)

        curr.prev = prev.node
        curr.score = prev.score
        curr.align1 = prev.align1
        curr.align2 = prev.align2

    # ------------------------------------ Deliverables -------------------------------------#
    def get_last_node(self):
        return self.table_graph[self.align_length1 - 1][self.align_length2 - 1]

    def get_final_score(self):
        return self.get_last_node().score

    def get_alignments(self):
        alignments = ['', '']
        prev = self.get_last_node()

        while prev is not None:
            alignments[0] += prev.align1
            alignments[1] += prev.align2

            prev = prev.prev

        for i in range(len(alignments)):
            alignments[i] = alignments[i][::-1]

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
                out += str(self.table_graph[i][j].score) + "\t"

            out += "\n"

        return out.expandtabs(8)

