#!/usr/bin/python3
from method.Banded import Banded
from method.Unrestricted import Unrestricted
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    pass
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class GeneSequencing:
    # Unrestricted: Time O(nm), Space O(nm)
    # Banded: Time O(kn), Space O(kn)
    def align(self, seq1, seq2, banded, align_length):
        # Time O(1), Space O(1)
        if banded:
            method = Banded(seq1, seq2, align_length)
        else:
            method = Unrestricted(seq1, seq2, align_length)

        # Unrestricted: Time O(nm), Space O(nm)
        # Banded: Time O(kn), Space O(kn)
        method.align()

        # Time O(1), Space O(1)
        score = method.get_score()

        # Time O(n + m), Space O(n + m)
        alignment1, alignment2 = method.get_alignments()

        print("Score: " + str(score))
        print("Alignment1: " + alignment1[:100])
        print("Alignment2: " + alignment2[:100])
        print()

        return {'align_cost': score,
                'seqi_first100': alignment1,
                'seqj_first100': alignment2}
