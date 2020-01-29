import sys
from mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # form
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionExit.setShortcut('Ctrl+Q')
        self.ui.actionAbout.setShortcut('Ctrl+A')
        self.ui.actionHelp.setShortcut('Ctrl+H')
        self.ui.actionSave.setShortcut('Ctrl+S')
        self.ui.actionSave_As.setShortcut('Ctrl+Alt+S')

        self.ui.radioButton_2.setChecked(1)
        self.currentencoding = QTextCodec.codecForName("CP1251")
        self.pathFile = QDir()

        self.colors = [QColor(0, 0, 0), QColor(214, 192, 24), QColor(119, 214, 24), QColor(24, 24, 214), QColor(214, 24, 24)]

        # tree view
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath('')
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.ui.treeView.setModel(self.model)

        # connects
        self.ui.actionAbout.triggered.connect(self.aboutMenu_on_clicked)
        self.ui.actionHelp.triggered.connect(self.helpMenu_on_clicked)
        self.ui.actionExit.triggered.connect(self.exitMenu_on_clicked)
        self.ui.actionSave.triggered.connect(self.saveMenu_on_clicked)
        self.ui.actionSave.triggered.connect(self.saveAsMenu_on_clicked)
        self.ui.treeView.clicked.connect(self.tree_view_element_on_clicked)
        self.ui.listWidget.clicked.connect(self.file_list_item_on_clicked)
        self.ui.checkBox.toggled.connect(self.on_boldBox_toggled)
        self.ui.checkBox_2.clicked.connect(self.on_italicBox_toggled)
        self.ui.checkBox_3.clicked.connect(self.on_underlineBox_toggled)
        self.ui.comboBox.currentIndexChanged.connect(self.on_combobox_currentIndexChanged)
        self.ui.pushButton.clicked.connect(self.on_defaultoptionsButton_clicked)
        self.ui.radioButton_2.toggled.connect(self.on_cpButton2_toogled)
        self.ui.radioButton.toggled.connect(self.on_cpButton1_toogled)

    def rewriteFile(self):
        fOut = QFile(self.pathFile)
        if(fOut.open(QIODevice.WriteOnly)):
            writestream = QTextStream(fOut)
            writestream.setAutoDetectUnicode(0)
            writestream.setCodec(self.currentencoding)
            writestream = self.ui.textEdit.toPlainText()
            fOut.flush()
            fOut.close()
        else:
            dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'Smth wrong',
                                           """File don't saved""")
            dialog.exec_()

    def saveAsMenu_on_clicked(self):
        fullPath = QFileDialog.getSaveFileName(self,'Save as..', (''), ("Text(*.txt)"))
        self.pathFile = fullPath
        self.rewriteFile()

    def saveMenu_on_clicked(self):
        self.rewriteFile()

    def aboutMenu_on_clicked(self):
        dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'About', 'Автор: Чуваев Павел\n'
                                                                                   'Группа: 8-Т3О-302Б-16')
        dialog.exec_()

    def exitMenu_on_clicked(self):
        sys.exit()

    def helpMenu_on_clicked(self):
        dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'Help', 'Лабораторная работа 1\n'
                                                                                  'Текстовый просмотрщик')
        dialog.exec_()

    def tree_view_element_on_clicked(self, index):
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.get_files_in_folder(index))

    def get_files_in_folder(self, index):
        self.pathDir = QDir(self.model.fileInfo(index).absoluteFilePath())
        self.pathDir.setFilter(QDir.Files)
        fileList = self.pathDir.entryList()
        return fileList

    def file_list_item_on_clicked(self, item):
        self.pathFile = self.pathDir.absolutePath() + "/" + self.ui.listWidget.item(self.ui.listWidget.currentRow()).text()
        self.readFile()

    def readFile(self):
        if '.txt' in self.pathFile:
            fIn = QFile(self.pathFile)
            if fIn.open(QFile.ReadOnly | QFile.Text):
                readstream = QTextStream(fIn)
                readstream.setAutoDetectUnicode(0)
                readstream.setCodec(self.currentencoding)
                self.ui.textEdit.setText(readstream.readAll())
            fIn.close()
        else:
            dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'Smth wrong', """You can check only .txt files""")
            dialog.exec_()

    def on_italicBox_toggled(self):
        cursor = QTextCursor(self.ui.textEdit.textCursor())
        self.ui.textEdit.selectAll()
        self.ui.textEdit.setFontItalic(not self.ui.textEdit.fontItalic())
        self.ui.textEdit.setTextCursor(cursor)
        self.ui.textEdit.setFocus()



    def on_boldBox_toggled(self, checked):
        cursor = QTextCursor(self.ui.textEdit.textCursor())
        self.ui.textEdit.selectAll()
        if checked:
            self.ui.textEdit.setFontWeight(QFont.Bold)
        else:
            self.ui.textEdit.setFontWeight(QFont.Normal)
        self.ui.textEdit.setTextCursor(cursor)
        self.ui.textEdit.setFocus()

    def on_underlineBox_toggled(self):
        cursor = QTextCursor(self.ui.textEdit.textCursor())
        self.ui.textEdit.selectAll()
        self.ui.textEdit.setFontUnderline(not self.ui.textEdit.fontUnderline())
        self.ui.textEdit.setTextCursor(cursor)
        self.ui.textEdit.setFocus()

    def on_cpButton2_toogled(self, checked):
        if checked:
            self.currentencoding = QTextCodec.codecForName("CP1251")
        else:
            self.currentencoding = QTextCodec.codecForName("UTF-8")
        self.readFile()

    def on_cpButton1_toogled(self, checked):
        if checked:
            self.currentencoding = QTextCodec.codecForName("UTF-8")
        else:
            self.currentencoding = QTextCodec.codecForName("CP1251")
        self.readFile()

    def on_combobox_currentIndexChanged(self, index):
        cursor = QTextCursor(self.ui.textEdit.textCursor())
        self.ui.textEdit.selectAll()
        self.ui.textEdit.setTextColor(self.GetColor(index))
        self.ui.textEdit.setTextCursor(cursor)
        self.ui.textEdit.setFocus()

    def on_defaultoptionsButton_clicked(self):
        cursor = QTextCursor(self.ui.textEdit.textCursor())
        self.ui.textEdit.selectAll()
        self.ui.textEdit.setFontWeight(QFont.Normal)
        self.ui.textEdit.setFontItalic(0)
        self.ui.textEdit.setFontUnderline(0)
        self.ui.textEdit.setTextColor(QColor(0, 0, 0))

        self.ui.checkBox.setChecked(0)
        self.ui.checkBox_2.setChecked(0)
        self.ui.checkBox_3.setChecked(0)
        self.ui.comboBox.setCurrentIndex(0)

        self.ui.textEdit.setTextCursor(cursor)
        self.ui.textEdit.setFocus()

    def GetColor(self, index):
        return self.colors[index]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
