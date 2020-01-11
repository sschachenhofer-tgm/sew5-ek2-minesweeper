# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customgame.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(276, 167)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 253, 142))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.mines_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.mines_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mines_label.setObjectName("mines_label")
        self.gridLayout.addWidget(self.mines_label, 2, 0, 1, 1)
        self.rows_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.rows_label.setAlignment(QtCore.Qt.AlignCenter)
        self.rows_label.setObjectName("rows_label")
        self.gridLayout.addWidget(self.rows_label, 1, 0, 1, 1)
        self.colummns_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colummns_label.sizePolicy().hasHeightForWidth())
        self.colummns_label.setSizePolicy(sizePolicy)
        self.colummns_label.setAlignment(QtCore.Qt.AlignCenter)
        self.colummns_label.setObjectName("colummns_label")
        self.gridLayout.addWidget(self.colummns_label, 0, 0, 1, 1)
        self.columns = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.columns.setMinimum(3)
        self.columns.setProperty("value", 9)
        self.columns.setObjectName("columns")
        self.gridLayout.addWidget(self.columns, 0, 1, 1, 1)
        self.rows = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.rows.setMinimum(3)
        self.rows.setProperty("value", 9)
        self.rows.setObjectName("rows")
        self.gridLayout.addWidget(self.rows, 1, 1, 1, 1)
        self.mines = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.mines.setMinimum(1)
        self.mines.setMaximum(9800)
        self.mines.setProperty("value", 10)
        self.mines.setObjectName("mines")
        self.gridLayout.addWidget(self.mines, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.mines_label.setText(_translate("Dialog", "Mines"))
        self.rows_label.setText(_translate("Dialog", "Rows"))
        self.colummns_label.setText(_translate("Dialog", "Columns"))

