from Node import Node
from ScoreEnum import Score


class TableGraph:
    def __int__(self, seq1, seq2):
        self.seq1 = seq1.insert(0, '-')
        self.seq2 = seq2.insert(0, '-')
        self.table_graph = []
        self.populate_table_graph()

    def populate_table_graph(self):
        for i in range(len(self.seq1)):
            for j in range(len(self.seq2)):
                self.table_graph[i][j] = Node(i, j)

    def align_edges(self):
        self.table_graph[0][0].score = 0

        for i in range(1, len(self.seq1)):
            self.table_graph[i][0].score = self.table_graph[i - 1][0].score + Score.INS_DEL

        for j in range(1, len(self.seq2)):
            self.table_graph[0][j].score = self.table_graph[0][j - 1].score + Score.INS_DEL

    def align(self):
        self.align_edges()

        for i in range(1, len(self.seq2)):
            for j in range(1, len(self.seq1)):
                self.align_node(i, j)

    # ------------------------------------- Calc Prevs --------------------------------------#
    def calc_upper_left(self, i, j):
        return self.table_graph[i - 1][j - 1]

    def calc_upper(self, i, j):
        return self.table_graph[i - 1][j]

    def calc_left(self, i, j):
        return self.table_graph[i][j - 1]

    # ---------------------------------- Calc Prev Scores -----------------------------------#\
    def calc_upper_left_score(self, upper_left):
        if self.seq1[upper_left.i] == self.seq2[upper_left.j]:
            return upper_left.score + Score.MATCH
        else:
            return upper_left.score + Score.SUB

    def calc_upper_score(self, upper):
        return upper.score + Score.INS_DEL

    def calc_left_score(self, left):
        return left.score + Score.INS_DEL

    # ------------------------------------ Calc Min Prev ------------------------------------#
    def calc_min_prev(self, i, j):
        upper_left = self.calc_upper_left(i, j)
        upper = self.calc_upper(i, j)
        left = self.calc_left(i, j)
        prevs = {upper_left: self.calc_upper_left_score(left),
                 upper: self.calc_upper_score(upper),
                 left: self.calc_left_score(left)}

        return min(prevs, key=prevs.get)

    # ---------------------------------- Align Node[i][j] -----------------------------------#
    def align_node(self, i, j):
        prev = self.calc_min_prev(i, j)
        self.table_graph[i][j].prev = prev[0]
        self.table_graph[i][j].score = prev[1]

    # ---------------------------------------- Debug ----------------------------------------#
    def to_string(self):
        out = ""

        for i in range(len(self.seq1)):
            for j in range(len(self.seq2)):
                out += str(self.table_graph[i][j].score) + " "
            out += "\n"

        return out

