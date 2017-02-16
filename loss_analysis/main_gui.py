import sys
import traceback
import os
from PyQt5.QtWidgets import (QWidget, QFileDialog, QPushButton, QTextEdit,
                             QGridLayout, QApplication, QLabel, QComboBox,
                             QCheckBox, QLineEdit)
# files for this package
import loss_analysis


class LoadButtonCombo(QWidget):
#TODO: couldn't this whole class just be a single function?

    def __init__(self, grid, info, default_file, row, column):
        super().__init__()

        self.info = info

        path = os.path.join(os.pardir, 'example_cell')
        self.filepath = os.path.join(path, default_file)

        self._add_objects(grid, row, column)

    def _add_objects(self, grid,  row, column):
        '''
        Builds and binds the boxes.
        '''
        self.btn = QPushButton('Load {0}'.format(self.info))
        self.btn.clicked.connect(self._get)

        filename = os.path.basename(self.filepath)

        self.label = QLabel(filename, self)
        grid.addWidget(self.btn, row, column)
        grid.addWidget(self.label, row, column + 1)

    def _get(self):
        '''
        Gets and sets the label with the new file name
        '''
        default_dir = os.path.dirname(self.filepath)
        self.filepath = QFileDialog.getOpenFileName(self, 'Choose {0} file'.format(self.info),
                                                    default_dir)[0]
        filename = os.path.basename(self.filepath)
        self.label.setText(filename)

    def file(self):
        return {self.info + '_fname': self.filepath}


class LossAnalysisGui(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        # grid.setSpacing(10)
        self.output_dir = os.path.join(os.pardir, 'example_cell')
        self.start_dir = os.path.join(os.pardir, 'example_cell')
        self.save_fig_bool = False

        boxes = [['reflectance', 'example_reflectance.csv'],
                 ['EQE', 'example_EQE.txt'],
                 ['light IV', 'example_lightIV.lgt'],
                 ['suns Voc', 'example_sunsVoc.xlsm'],
                 ['dark IV', 'example_darkIV.drk']
                 ]

        self.items = []

        # TODO Ned: I'm not convinced this is the best method
        for box, row_num in zip(boxes, range(len(boxes))):
            self.items.append(LoadButtonCombo(grid, box[0], box[1],
                                              row_num + 1, 0))

        # select starting directory
        self.btn_start_dir = QPushButton("Select start directory")
        self.btn_start_dir.clicked.connect(self.select_start_dir)
        grid.addWidget(self.btn_start_dir, 6, 0)
        self.label_start_dir = QLabel(os.path.basename(self.start_dir), self)
        grid.addWidget(self.label_start_dir, 6, 1)

        # cell name input
        self.cell_name_input = QLineEdit(self)
        grid.addWidget(self.cell_name_input, 7, 1)

        # select output directory
        self.btn_output_dir = QPushButton("Select output directory")
        self.btn_output_dir.clicked.connect(self.select_output_dir)
        grid.addWidget(self.btn_output_dir, 8, 0)
        self.label_output_dir = QLabel(os.path.basename(self.output_dir), self)
        grid.addWidget(self.label_output_dir, 8, 1)

        # save figures checkbox
        self.cb_save_fig = QCheckBox('Save figures', self)
        self.cb_save_fig.stateChanged.connect(self.save_fig_toggle)
        grid.addWidget(self.cb_save_fig, 9, 0)

        # process all data
        self.btn_process = QPushButton("Process data")
        self.btn_process.clicked.connect(self.process_data)
        grid.addWidget(self.btn_process, 10, 0)

        self.setLayout(grid)
        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('Loss analysis')
        self.show()

    def select_start_dir(self):
        self.start_dir = QFileDialog.getExistingDirectory(self,
                        'Choose start directory', self.start_dir)
        self.label_start_dir.setText(os.path.basename(self.start_dir))

    def select_output_dir(self):
        self.output_dir = QFileDialog.getExistingDirectory(self,
                        'Choose output directory', self.output_dir)
        self.label_output_dir.setText(os.path.basename(self.output_dir))

    def save_fig_toggle(self, state):
        if self.cb_save_fig.isChecked():
            self.save_fig_bool = True
        else:
            self.save_fig_bool = False

    def process_data(self):

        files = {}
        for i in self.items:
            files.update(i.file())

        # pass the file names, and let the next thing handle them.
        la = loss_analysis.Cell(**files)
        if self.cell_name_input.text()=='':
            cell_name = None
        la.process_all(self.save_fig_bool, self.output_dir,
                       self.cell_name_input.text())


if __name__ == '__main__':

    logfile = open('traceback_log.txt', 'w')
    app = QApplication(sys.argv)
    # try:
    ex = LossAnalysisGui()
    # except:
    # traceback.print_exc(file=logfile)

    ex.show()
    logfile.close()
    sys.exit(app.exec_())