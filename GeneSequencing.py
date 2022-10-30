#!/usr/bin/python3
from Banded import Banded
from Unrestricted import Unrestricted
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt6.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time
import random


class GeneSequencing:
    def __init__(self):
        self.banded = None

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        if banded:
            method = Banded(seq1, seq2, align_length)
        else:
            method = Unrestricted(seq1, seq2, align_length)

        method.align()

        print(method.to_string())

        score = method.get_score()
        alignment1, alignment2 = method.get_alignments()

        print("Score: " + str(score))
        print("Alignment 1: " + alignment1[0:100])
        print("Alignment 2: " + alignment2[0:100])
        print()

        return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
