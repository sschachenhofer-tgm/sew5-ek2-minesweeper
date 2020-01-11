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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 551, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 569, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        self.new_game = QtWidgets.QMenu(self.menubar)
        self.new_game.setObjectName("new_game")
        MainWindow.setMenuBar(self.menubar)
        self.action_new_game = QtWidgets.QAction(MainWindow)
        self.action_new_game.setObjectName("action_new_game")
        self.new_game_easy = QtWidgets.QAction(MainWindow)
        self.new_game_easy.setObjectName("new_game_easy")
        self.new_game_medium = QtWidgets.QAction(MainWindow)
        self.new_game_medium.setObjectName("new_game_medium")
        self.new_game_difficult = QtWidgets.QAction(MainWindow)
        self.new_game_difficult.setObjectName("new_game_difficult")
        self.new_game_custom = QtWidgets.QAction(MainWindow)
        self.new_game_custom.setObjectName("new_game_custom")
        self.new_game.addAction(self.new_game_easy)
        self.new_game.addAction(self.new_game_medium)
        self.new_game.addAction(self.new_game_difficult)
        self.new_game.addAction(self.new_game_custom)
        self.menubar.addAction(self.new_game.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minesweeper"))
        self.new_game.setTitle(_translate("MainWindow", "New game"))
        self.action_new_game.setText(_translate("MainWindow", "Start new game"))
        self.new_game_easy.setText(_translate("MainWindow", "Easy (9x9, 10 mines)"))
        self.new_game_medium.setText(_translate("MainWindow", "Medium (16x16, 40 mines)"))
        self.new_game_difficult.setText(_translate("MainWindow", "Difficult (30x16, 99 mines)"))
        self.new_game_custom.setText(_translate("MainWindow", "Custom"))

