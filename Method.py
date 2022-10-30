from abc import ABC, abstractmethod

MATCH = -3
INS_DEL = 5
SUB = 1


class Method(ABC):
    def __init__(self, seq1, seq2, align_length):
        self.seq1 = '-' + seq1
        self.seq2 = '-' + seq2
        self.seq1_length = len(seq1)
        self.seq2_length = len(seq2)
        self.align_length1 = min(self.seq1_length + 1, align_length + 1)
        self.align_length2 = self.calc_align_length2(align_length)
        self.scores = {}
        self.prevs = {}

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                         Align                                          #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    @abstractmethod
    def calc_align_length2(self, align_length):
        pass

    def calc_diagonal_score(self, i, j):
        diagonal_score = self.scores[i - 1, j - 1]
        align1 = self.seq1[i]
        align2 = self.seq2[j]

        return diagonal_score + MATCH if align1 == align2 else diagonal_score + SUB

    @abstractmethod
    def calc_prevs(self, i, j):
        pass

    def calc_min_prev(self, i, j):
        score = 0
        prev_char = 1
        priority = 2
        prevs = self.calc_prevs(i, j)

        min_prev = prevs.pop()
        for prev in prevs:
            if prev[score] < min_prev[score] or \
                    (prev[score] == min_prev[score] and prev[priority] < min_prev[priority]):
                min_prev = prev

        return min_prev[score], min_prev[prev_char]

    def align_initial(self):
        self.scores[0, 0] = 0
        self.prevs[0, 0] = None

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                     Deliverables                                       #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    def get_score(self):
        return self.scores[self.align_length1 - 1, self.align_length2 - 1]

    def get_alignments(self):
        alignment1 = ''
        alignment2 = ''
        i = self.align_length1 - 1
        j = self.align_length2 - 1
        curr = self.prevs[i, j]

        while curr is not None:
            if curr == 'D':
                alignment1 = self.seq1[i] + alignment1
                alignment2 = self.seq2[j] + alignment2
                i -= 1
                j -= 1

            elif curr == 'U':
                alignment1 = self.seq1[i] + alignment1
                alignment2 = '-' + alignment2
                i -= 1

            elif curr == 'L':
                alignment1 = '-' + alignment1
                alignment2 = self.seq2[j] + alignment2
                j -= 1

            curr = self.prevs[i, j]

        return alignment1, alignment2

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                         Debug                                          #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    def calc_top_row_string(self, initial_index2, end_index2):
        out = " \t"

        for j in range(initial_index2, end_index2):
            out += self.seq2[j] + "\t"

        out += "\n"

        return out

    def calc_string(self, initial_index1, end_index1, initial_index2, end_index2):
        out = self.calc_top_row_string(initial_index2, end_index2)

        # Print rest of table
        for i in range(initial_index1, end_index1):

            out += self.seq1[i] + "\t"

            for j in range(initial_index2, end_index2):
                cell = self.scores.get((i, j))

                if cell is None:
                    out += "-\t"
                else:
                    out += str(cell) + "\t"

            out += "\n"

        return out

    def to_string(self):
        out = ''

        if self.align_length1 > 20 or self.align_length2 > 20:
            out += "Initial\n"
            out += self.calc_string(0, min(self.align_length1, 20),
                                    0, min(self.align_length2, 20)) + "\n"

            out += "End\n"
            out += self.calc_string(self.align_length1 - 20, self.align_length1,
                                    self.align_length2 - 20, self.align_length2)

        else:
            out += self.calc_string(0, self.align_length1,
                                    0, self.align_length2)

        return out.expandtabs(8)
