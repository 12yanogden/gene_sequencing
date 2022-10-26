#!/usr/bin/python3
from TableGraph import TableGraph
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time
import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


class GeneSequencing:
	def __init__(self):
		self.banded = None
		self.MaxCharactersToAlign = None
	
# This is the method called by the GUI.
	# _seq1_ and _seq2_ are two sequences to be aligned
	# _banded_ is a boolean that tells you whether you should compute a banded alignment or full alignment
	# _align_length_ tells you how many base pairs to use in computing the alignment

	def align(self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length

		table_graph = TableGraph(seq1, seq2, align_length)

		table_graph.align()

		# print(table_graph.to_string())

		score = table_graph.get_final_score()

		alignments = table_graph.get_alignments()
		alignment1 = alignments[0]
		alignment2 = alignments[1]

		# print("alignment1: " + alignment1)
		# print("alignment2: " + alignment2)
		# print("score: " + str(score))
		# print()

		return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}


