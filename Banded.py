class Banded:
    def __init__(self, seq1, seq2, align_length):
        self.seq1 = '-' + seq1
        self.seq2 = '-' + seq2
        self.seq1_length = len(seq1)
        self.seq2_length = len(seq2)
        self.align_length1 = min(self.seq1_length + 1, align_length + 1)
        self.align_length2 = min(self.seq2_length + 1, align_length + 1, self.align_length1 + 3)
        self.scores = {}
        self.prevs = {}

    # ---------------------------------------------------------------------------------------#
    #                                                                                        #
    #                                         Align                                          #
    #                                                                                        #
    # ---------------------------------------------------------------------------------------#
    def align(self):
        second_third_section_border = self.align_length1 - 3

        # Align initial
        self.scores[0, 0] = 0
        self.prevs[0, 0] = None

        # Align edge scores
        for i in range(1, 4):
            self.scores[i, 0] = i * 5
            self.prevs[i, 0] = 'U'
        for j in range(1, 4):
            self.scores[0, j] = j * 5
            self.prevs[0, j] = 'L'

        # Align first section
        for i in range(1, 4):
            for j in range(1, 4 + i):
                diagonal_score = self.scores[i - 1, j - 1]
                prevs = [[diagonal_score - 3 if self.seq1[i] == self.seq2[j] else diagonal_score + 1, 'D', 2]]

                if (i + 3) != j:
                    prevs.append([self.scores[i - 1, j] + 5, 'U', 1])

                if (i - 3) != j:
                    prevs.append([self.scores[i, j - 1] + 5, 'L', 0])

                min_prev = prevs.pop()
                for prev in prevs:
                    if prev[0] < min_prev[0] or \
                            (prev[0] == min_prev[0] and prev[2] < min_prev[2]):
                        min_prev = prev

                self.scores[i, j] = min_prev[0]
                self.prevs[i, j] = min_prev[1]

        # Align second section
        for i in range(4, second_third_section_border):
            for j in range(i - 3, i + 4):
                diagonal_score = self.scores[i - 1, j - 1]
                prevs = [[diagonal_score - 3 if self.seq1[i] == self.seq2[j] else diagonal_score + 1, 'D', 2]]

                if (i + 3) != j:
                    prevs.append([self.scores[i - 1, j] + 5, 'U', 1])

                if (i - 3) != j:
                    prevs.append([self.scores[i, j - 1] + 5, 'L', 0])

                min_prev = prevs.pop()
                for prev in prevs:
                    if prev[0] < min_prev[0] or \
                            (prev[0] == min_prev[0] and prev[2] < min_prev[2]):
                        min_prev = prev

                self.scores[i, j] = min_prev[0]
                self.prevs[i, j] = min_prev[1]

        # Align third section
        for i in range(second_third_section_border, self.align_length1):
            for j in range(i - 3, min(i + 4, self.align_length2)):
                diagonal_score = self.scores[i - 1, j - 1]
                prevs = [[diagonal_score - 3 if self.seq1[i] == self.seq2[j] else diagonal_score + 1, 'D', 2]]

                if (i + 3) != j:
                    prevs.append([self.scores[i - 1, j] + 5, 'U', 1])

                if (i - 3) != j:
                    prevs.append([self.scores[i, j - 1] + 5, 'L', 0])

                min_prev = prevs.pop()
                for prev in prevs:
                    if prev[0] < min_prev[0] or \
                            (prev[0] == min_prev[0] and prev[2] < min_prev[2]):
                        min_prev = prev

                self.scores[i, j] = min_prev[0]
                self.prevs[i, j] = min_prev[1]

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
