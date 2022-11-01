from method.Method import Method

MATCH = -3
INS_DEL = 5
SUB = 1


class Unrestricted(Method):
    # Time: O(1), Space: O(1)
    def calc_align_length2(self, align_length):
        return min(self.seq2_length + 1, align_length + 1)

    # -----------------------------------------------------------------------------#
    #                                                                              #
    #                                    Align                                     #
    #                                                                              #
    # -----------------------------------------------------------------------------#
    # Time: O(1), Space: O(1)
    def calc_prevs(self, i, j):
        return [[self.calc_diagonal_score(i, j), 'D', 2],
                [self.scores[i - 1, j] + INS_DEL, 'U', 1],
                [self.scores[i, j - 1] + INS_DEL, 'L', 0]]

    # Time O(nm), Space O(nm)
    def align(self):
        self.align_initial()

        # ------------------------------ Align edges ------------------------------#
        # Time O(n), Space O(n)
        for i in range(1, self.align_length1):
            self.scores[i, 0] = i * INS_DEL
            self.prevs[i, 0] = 'U'

        # Time O(m), Space O(m)
        for j in range(1, self.align_length2):
            self.scores[0, j] = j * INS_DEL
            self.prevs[0, j] = 'L'

        # ------------------------------ Align rest -------------------------------#
        # Time O(nm), Space O(nm)
        for i in range(1, self.align_length1):
            for j in range(1, self.align_length2):
                prev_score, prev_char = self.calc_min_prev(i, j)

                self.scores[i, j] = prev_score
                self.prevs[i, j] = prev_char
