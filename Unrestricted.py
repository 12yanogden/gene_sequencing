MATCH = -3
INS_DEL = 5
SUB = 1


class Unrestricted:
    def __init__(self, seq1, seq2, align_length):
        self.seq1 = '-' + seq1
        self.seq2 = '-' + seq2
        self.seq1_length = len(seq1)
        self.seq2_length = len(seq2)
        self.align_length1 = min(self.seq1_length + 1, align_length + 1)
        self.align_length2 = min(self.seq2_length + 1, align_length + 1)
        self.scores = {}
        self.prevs = {}

    def calc_diagonal_score(self, diagonal_score, align1, align2):
        if align1 == align2:
            return diagonal_score + MATCH
        else:
            return diagonal_score + SUB

    def calc_min_score(self, i, j, align1, align2):
        prevs = [[self.calc_diagonal_score(self.scores[i - 1, j - 1], align1, align2), 'D', 2],
                 [self.scores[i - 1, j] + INS_DEL, 'U', 1],
                 [self.scores[i, j - 1] + INS_DEL, 'L', 0]]

        min_prev = prevs[0]
        for prev in prevs:
            if prev[0] < min_prev[0] or \
                    (prev[0] == min_prev[0] and prev[1] < min_prev[1]):
                min_prev = prev

        return min_prev[0], min_prev[1]

    def align(self):
        # Initial score
        self.scores[0, 0] = 0
        self.prevs[0, 0] = None

        # Edge scores
        for i in range(1, self.align_length1):
            self.scores[i, 0] = i * INS_DEL
            self.prevs[i, 0] = 'L'
        for j in range(1, self.align_length2):
            self.scores[0, j] = j * INS_DEL
            self.prevs[0, j] = 'U'

        # Fill in the rest of the scores
        for i in range(1, self.align_length1):
            for j in range(1, self.align_length2):
                min_score, prev_char = self.calc_min_score(i, j, self.seq1[i], self.seq2[j])

                self.scores[i, j] = min_score
                self.prevs[i, j] = prev_char

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
                j -= 1

            elif curr == 'L':
                alignment1 = '-' + alignment1
                alignment2 = self.seq2[j] + alignment2
                i -= 1

            curr = self.prevs[i, j]

        return alignment1, alignment2

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
                out += str(self.scores[i, j]) + "\t"

            out += "\n"

        return out.expandtabs(8)
