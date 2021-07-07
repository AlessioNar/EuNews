from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import os
import csv
from sys import argv
script, filename = argv

# CSV file model
class CsvTableModel(QtCore.QAbstractTableModel):
    """The model for a CSV table."""

    def __init__(self, csv_file):
        super().__init__()
        self.filename = csv_file
        with open(self.filename) as fh:
            csvreader = csv.reader(fh)
            self._headers = next(csvreader)
            self._data = list(csvreader)

    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return self._data[index.row()][index.column()]

    # Additional features methods:

    def headerData(self, section, orientation, role):

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()  # needs to be emitted before a sort
        self._data.sort(key=lambda x: x[column])
        if order == QtCore.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # needs to be emitted after a sort

    # Methods for Read/Write

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    # Methods for inserting or deleting

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(
            parent or QtCore.QModelIndex(),
            position,
            position + rows - 1
        )

        for i in range(rows):
            default_row = [''] * len(self._headers)
            self._data.insert(position, default_row)
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(
            parent or QtCore.QModelIndex(),
            position,
            position + rows - 1
        )
        for i in range(rows):
            del(self._data[position])
        self.endRemoveRows()

    # method for saving
    def save_data(self):
        # commented out code below to fix issue with additional lines being added after saving csv file from the window.
        # with open(self.filename, 'w', encoding='utf-8') as fh:
        with open(self.filename, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow(self._headers)
            writer.writerows(self._data)



class MainWindow(QtWidgets.QMainWindow):
    # Define main window
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Set table view
        self.tableview = QtWidgets.QTableView()
        self.tableview.setSortingEnabled(True)

        self.pdf = QWebEngineView()

        # Create grid
        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(self.tableview, 0, 0)
        lay.addWidget(self.pdf, 0, 1)

        # Set column stretch
        lay.setColumnStretch(0, 2)
        lay.setColumnStretch(1, 1)


        # Setup the menu
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        file_menu.addAction('Open', self.select_file)
        file_menu.addAction('Save', self.save_file, 'CTRL+S')
        file_menu.addAction('Show PDF', self.render_pdf, 'CTRL+Q')

        edit_menu = menu.addMenu('Edit')
        edit_menu.addAction('Insert Below', self.insert_below, 'CTRL+L')
        edit_menu.addAction('Remove Row(s)', self.remove_rows, 'CTRL+W')

        # Render the csv file
        self.model = CsvTableModel(filename)
        self.tableview.setModel(self.model)

    # File methods
    def select_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Select a CSV file to open…',
            QtCore.QDir.currentPath(),
            'CSV Files (*.csv) ;; All Files (*)'
        )
        if filename:
            self.model = CsvTableModel(filename)
            self.tableview.setModel(self.model)

    def save_file(self):
        if self.model:
            self.model.save_data()

    # Methods for insert/remove

    def insert_below(self):
        selected = self.tableview.selectedIndexes()
        row = selected[-1].row() if selected else self.model.rowCount(None)
        self.model.insertRows(row + 1, 1, None)

    def remove_rows(self):
        selected = self.tableview.selectedIndexes()
        num_rows = len(set(index.row() for index in selected))
        if selected:
            self.model.removeRows(selected[0].row(), num_rows, None)

    def render_pdf(self):
        selected = self.tableview.selectedIndexes()
        if selected:
            model = self.tableview.model()
            index = model.index(selected[0].row(), 3)
            url = str(model.data(index, QtCore.Qt.DisplayRole))

            ## This works I just need to find the url
            self.pdf.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            self.pdf.load(QtCore.QUrl(url))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
