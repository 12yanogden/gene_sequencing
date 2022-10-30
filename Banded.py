MATCH = -3
INS_DEL = 5
SUB = 1

MAX_INS_DEL = 3
BAND_RADIUS = MAX_INS_DEL + 1
BAND_WIDTH = 2 * MAX_INS_DEL + 1


class Banded:
    def __init__(self, seq1, seq2, align_length):
        self.seq1 = '-' + seq1
        self.seq2 = '-' + seq2
        self.seq1_length = len(seq1)
        self.seq2_length = len(seq2)
        self.align_length1 = min(self.seq1_length + 1, align_length + 1)
        self.align_length2 = min(self.seq2_length + 1, align_length + 1, self.align_length1 + MAX_INS_DEL)
        self.scores = {}
        self.prevs = {}

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                         Align                                          #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    def calc_diagonal_score(self, i, j):
        diagonal_score = self.scores[i - 1, j - 1]
        align1 = self.seq1[i]
        align2 = self.seq2[j]

        return diagonal_score + MATCH if align1 == align2 else diagonal_score + SUB

    def calc_prevs(self, i, j):
        prevs = [[self.calc_diagonal_score(i, j), 'D', 2]]

        if (i + MAX_INS_DEL) != j:
            prevs.append([self.scores[i - 1, j] + INS_DEL, 'U', 1])

        if (i - MAX_INS_DEL) != j:
            prevs.append([self.scores[i, j - 1] + INS_DEL, 'L', 0])

        return prevs

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

    def align_cell(self, i, j):
        prev_score, prev_char = self.calc_min_prev(i, j)

        self.scores[i, j] = prev_score
        self.prevs[i, j] = prev_char

    def align(self):
        # Align initial
        self.scores[0, 0] = 0
        self.prevs[0, 0] = None

        # Align edge scores
        for i in range(1, BAND_RADIUS):
            self.scores[i, 0] = i * INS_DEL
            self.prevs[i, 0] = 'U'
        for j in range(1, BAND_RADIUS):
            self.scores[0, j] = j * INS_DEL
            self.prevs[0, j] = 'L'

        # Align first section
        for i in range(1, BAND_RADIUS):
            for j in range(1, BAND_RADIUS + i):
                self.align_cell(i, j)

        # Align second section
        for i in range(BAND_RADIUS, self.align_length1 - MAX_INS_DEL):
            for j in range(i - MAX_INS_DEL, i + BAND_RADIUS):
                self.align_cell(i, j)

        if self.align_length2 >= self.align_length1 + MAX_INS_DEL:
            # Continue to align second section
            for i in range(self.align_length1 - MAX_INS_DEL, self.align_length1):
                for j in range(i - MAX_INS_DEL, i + BAND_RADIUS):
                    self.align_cell(i, j)
        else:
            # Align third section
            for i in range(self.align_length1 - MAX_INS_DEL, self.align_length1):
                for j in range(i - MAX_INS_DEL, self.align_length2):
                    self.align_cell(i, j)

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
    def calc_top_row_string(self):
        out = " \t"

        for j in range(min(self.align_length2, 20)):
            out += self.seq2[j] + "\t"

        out += "\n"

        return out

    def calc_string(self, initial_index1, align_length1, initial_index2, align_length2):
        out = self.calc_top_row_string()

        # Print rest of table
        for i in range(initial_index1, align_length1):

            out += self.seq1[i] + "\t"

            for j in range(initial_index2, align_length2):
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
