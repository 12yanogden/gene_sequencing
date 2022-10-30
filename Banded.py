from Method import Method

MATCH = -3
INS_DEL = 5
SUB = 1

MAX_INS_DEL = 3
BAND_RADIUS = MAX_INS_DEL + 1
BAND_WIDTH = 2 * MAX_INS_DEL + 1


class Banded(Method):
    def calc_align_length2(self, align_length):
        return min(self.seq2_length + 1, align_length + 1, self.align_length1 + MAX_INS_DEL)

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                         Align                                          #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    def calc_prevs(self, i, j):
        prevs = [[self.calc_diagonal_score(i, j), 'D', 2]]

        if (i + MAX_INS_DEL) != j:
            prevs.append([self.scores[i - 1, j] + INS_DEL, 'U', 1])

        if (i - MAX_INS_DEL) != j:
            prevs.append([self.scores[i, j - 1] + INS_DEL, 'L', 0])

        return prevs

    def align_cell(self, i, j):
        prev_score, prev_char = self.calc_min_prev(i, j)

        self.scores[i, j] = prev_score
        self.prevs[i, j] = prev_char

    def align(self):
        self.align_initial()

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
