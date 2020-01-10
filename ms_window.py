# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'minesweeper.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(569, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 551, 531))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.columns = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.columns.setContentsMargins(0, 0, 0, 0)
        self.columns.setObjectName("columns")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 569, 26))
        self.menubar.setObjectName("menubar")
        self.new_game = QtWidgets.QMenu(self.menubar)
        self.new_game.setObjectName("new_game")
        MainWindow.setMenuBar(self.menubar)
        self.action_new_game = QtWidgets.QAction(MainWindow)
        self.action_new_game.setObjectName("action_new_game")
        self.new_game.addAction(self.action_new_game)
        self.menubar.addAction(self.new_game.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minesweeper"))
        self.new_game.setTitle(_translate("MainWindow", "New game"))
        self.action_new_game.setText(_translate("MainWindow", "Start new game"))

