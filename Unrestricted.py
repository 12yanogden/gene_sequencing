from Method import Method

MATCH = -3
INS_DEL = 5
SUB = 1


class Unrestricted(Method):
    def calc_align_length2(self, align_length):
        return min(self.seq2_length + 1, align_length + 1)

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                         Align                                          #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    def calc_prevs(self, i, j):
        return [[self.calc_diagonal_score(i, j), 'D', 2],
                [self.scores[i - 1, j] + INS_DEL, 'U', 1],
                [self.scores[i, j - 1] + INS_DEL, 'L', 0]]

    def align(self):
        self.align_initial()

        # Edge scores
        for i in range(1, self.align_length1):
            self.scores[i, 0] = i * INS_DEL
            self.prevs[i, 0] = 'U'
        for j in range(1, self.align_length2):
            self.scores[0, j] = j * INS_DEL
            self.prevs[0, j] = 'L'

        # Fill in the rest of the scores
        for i in range(1, self.align_length1):
            for j in range(1, self.align_length2):
                prev_score, prev_char = self.calc_min_prev(i, j)

                self.scores[i, j] = prev_score
                self.prevs[i, j] = prev_char
