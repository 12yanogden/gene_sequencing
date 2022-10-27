#!/usr/bin/env python3

import signal
import sys

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

# TODO: Error checking on txt boxes
# TODO: Color strings


# Import in the code with the actual implementation
from GeneSequencing import *


# from GeneSequencing_complete import *


class Proj4GUI(QMainWindow):

    def __init__(self):
        super(Proj4GUI, self).__init__()

        self.statusBar = None
        self.table = None
        self.processButton = None
        self.clearButton = None
        self.banded = None
        self.alignLength = None
        self.seq1_name = None
        self.seq1_chars = None
        self.seq2_chars = None
        self.seq2_name = None
        self.seq1n_lbl = None
        self.seq1c_lbl = None
        self.seq2c_lbl = None
        self.seq2n_lbl = None
        self.seq2n_lbl = None

        self.RED_STYLE = "background-color: rgb(255, 220, 220)"
        self.PLAIN_STYLE = "background-color: rgb(255, 255, 255)"

        self.seqs = self.load_sequences_from_file()
        self.processed_results = []

        self.init_ui()
        self.solver = GeneSequencing()

    def process_clicked(self):
        sequences = [self.seqs[i][2] for i in sorted(self.seqs.keys())]

        # TODO: validate alignLength
        self.statusBar.showMessage('Processing...')
        app.processEvents()
        start = time.time()

        for i in range(len(sequences)):
            j_results = []
            for j in range(len(sequences)):
                if j < i:
                    s = {}
                else:
                    s = self.solver.align(sequences[i], sequences[j], banded=self.banded.isChecked(),
                                          align_length=int(self.alignLength.text()))
                    self.table.item(i, j).setText(
                        '{}'.format(int(s['align_cost']) if s['align_cost'] != math.inf else s['align_cost']))
                    # table.repaint()
                    app.processEvents()
                j_results.append(s)
            self.processed_results.append(j_results)

        end = time.time()
        ns = end - start
        nm = math.floor(ns / 60.)
        ns = ns - 60. * nm
        if nm > 0:
            self.statusBar.showMessage('Done.  Time taken: {} minutes and {:3.3f} seconds.'.format(nm, ns))
        else:
            self.statusBar.showMessage('Done.  Time taken: {:3.3f} seconds.'.format(ns))
        self.processButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.repaint()

    def clear_clicked(self):
        self.processed_results = []
        self.reset_table()
        self.processButton.setEnabled(True)
        self.clearButton.setEnabled(False)

        self.seq1n_lbl.setText('Label {}: '.format('I'))
        self.seq1c_lbl.setText('Sequence {}: '.format('I'))
        self.seq2c_lbl.setText('Sequence {}: '.format('J'))
        self.seq2n_lbl.setText('Label {}: '.format('J'))

        self.seq1_name.setText('{}'.format(' '))
        self.seq2_name.setText('{}'.format(' '))
        self.seq1_chars.setText('{}'.format(' '))
        self.seq2_chars.setText('{}'.format(' '))
        self.statusBar.showMessage('')
        self.repaint()

    def reset_table(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if j >= i:
                    self.table.item(i, j).setText(' ')

    def cell_clicked(self, i, j):
        print('Cell {},{} clicked!'.format(i, j))
        print('lbls: {} and {}'.format(self.seqs[i][1], self.seqs[j][1]))

        if self.processed_results and j >= i:
            print('in if')
            self.seq1n_lbl.setText('Label {}: '.format(i + 1))
            self.seq1c_lbl.setText('Sequence {}: '.format(i + 1))
            self.seq2c_lbl.setText('Sequence {}: '.format(j + 1))
            self.seq2n_lbl.setText('Label {}: '.format(j + 1))

            self.seq1_name.setText('{}'.format(self.seqs[i][1]))
            self.seq2_name.setText('{}'.format(self.seqs[j][1]))
            results = self.processed_results[i][j]
            self.seq1_chars.setText('{}'.format(results['seqi_first100']))
            self.seq2_chars.setText('{}'.format(results['seqj_first100']))

    def load_sequences_from_file(self):
        filename = 'genomes.txt'
        raw = open(filename, 'r').readlines()
        sequences = {}

        i = 0
        cur_id = ''
        cur_str = ''
        for liner in raw:
            line = liner.strip()
            if '#' in line:
                if len(cur_id) > 0:
                    sequences[i] = (i, cur_id, cur_str)
                    cur_str = ''
                    i += 1
                parts = line.split('#')
                cur_id = parts[0]
                cur_str += parts[1]
            else:
                cur_str += line
        if len(cur_str) > 0 or len(cur_id) > 0:
            sequences[i] = (i, cur_id, cur_str)
        return sequences

    def get_table_dims(self):
        width = self.table.columnWidth(self.table.rowCount() - 1) - 4
        for i in range(self.table.columnCount()):
            width += self.table.columnWidth(i)
        height = self.table.horizontalHeader().height() + 1
        for i in range(self.table.rowCount()):
            height += self.table.rowHeight(i)
        return width, height

    def init_ui(self):
        self.setWindowTitle('Gene Sequence Alignment')
        self.setWindowIcon(QIcon('icon312.png'))

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        vbox = QVBoxLayout()
        box_widget = QWidget()
        box_widget.setLayout(vbox)
        self.setCentralWidget(box_widget)

        self.table = QTableWidget(self)
        n_seq = 10
        self.table.setRowCount(n_seq)
        self.table.setColumnCount(n_seq)

        headers = ['sequence{}'.format(a + 1) for a in range(n_seq)]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels(headers)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        for i in range(n_seq):
            for j in range(n_seq):
                q_item = QTableWidgetItem(" ")
                q_item.setFlags( Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                if j < i:
                    q_item.setBackground(QColor(200, 200, 200))
                    q_item.setFlags(Qt.ItemFlag.ItemIsSelectable)
                self.table.setItem(i, j, q_item)
        for i in range(n_seq):
            self.table.resizeColumnToContents(i)
        for j in range(n_seq):
            self.table.resizeRowToContents(i)                    # TODO: Is this right? or is this supposed to be nested?

        width, height = self.get_table_dims()
        self.table.setFixedWidth(width)
        self.table.setFixedHeight(height)

        self.processButton = QPushButton('Process')
        self.clearButton = QPushButton('Clear')

        self.banded = QCheckBox('Banded')
        self.banded.setChecked(False)
        self.alignLength = QLineEdit('1000')
        font = QFont()
        font.setFamily("Menlo")
        self.seq1_name = QLineEdit('')
        self.seq1_name.setFixedWidth(650)
        self.seq1_name.setEnabled(False)
        self.seq1_chars = QLineEdit('')
        self.seq1_chars.setFixedWidth(850)
        self.seq1_chars.setFont(font)
        self.seq1_chars.setEnabled(False)
        self.seq2_chars = QLineEdit('')
        self.seq2_chars.setFixedWidth(850)
        self.seq2_chars.setFont(font)
        self.seq2_chars.setEnabled(False)
        self.seq2_name = QLineEdit('')
        self.seq2_name.setFixedWidth(650)
        self.seq2_name.setEnabled(False)

        height = QHBoxLayout()
        height.addStretch(1)
        height.addWidget(self.table)
        height.addStretch(1)
        vbox.addLayout(height)

        height = QHBoxLayout()
        v_left = QVBoxLayout()
        v_right = QVBoxLayout()
        self.seq1n_lbl = QLabel('Label I: ')
        v_left.addWidget(self.seq1n_lbl)
        v_right.addWidget(self.seq1_name)

        self.seq1c_lbl = QLabel('Sequence I: ')
        v_left.addWidget(self.seq1c_lbl)
        v_right.addWidget(self.seq1_chars)

        self.seq2c_lbl = QLabel('Sequence J: ')
        v_left.addWidget(self.seq2c_lbl)
        v_right.addWidget(self.seq2_chars)

        self.seq2n_lbl = QLabel('Label J: ')
        v_left.addWidget(self.seq2n_lbl)
        v_right.addWidget(self.seq2_name)

        height.addLayout(v_left)
        height.addLayout(v_right)
        vbox.addLayout(height)

        height = QHBoxLayout()
        height.addStretch(1)
        height.addWidget(self.processButton)
        height.addWidget(self.clearButton)
        height.addStretch(1)
        vbox.addLayout(height)

        height = QHBoxLayout()
        height.addStretch(1)
        height.addWidget(self.banded)
        height.addWidget(QLabel('Align Length: '))
        height.addWidget(self.alignLength)
        height.addStretch(1)
        vbox.addLayout(height)

        self.processButton.clicked.connect(self.process_clicked)
        self.clearButton.clicked.connect(self.clear_clicked)
        self.clearButton.setEnabled(False)
        self.table.cellClicked.connect(self.cell_clicked)

        self.show()


if __name__ == '__main__':
    # This line allows Control-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    w = Proj4GUI()
    sys.exit(app.exec())
