# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/myfiberDialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(337, 305)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header_pic = QtWidgets.QLabel(Dialog)
        self.header_pic.setText("")
        self.header_pic.setObjectName("header_pic")
        self.verticalLayout.addWidget(self.header_pic)
        self.key_group = QtWidgets.QGroupBox(Dialog)
        self.key_group.setObjectName("key_group")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.key_group)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.key_text = QtWidgets.QLineEdit(self.key_group)
        self.key_text.setObjectName("key_text")
        self.verticalLayout_2.addWidget(self.key_text)
        self.api_group = QtWidgets.QGroupBox(self.key_group)
        self.api_group.setObjectName("api_group")
        self.gridLayout = QtWidgets.QGridLayout(self.api_group)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.api_group)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.api_group)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.text_path = QtWidgets.QLineEdit(self.api_group)
        self.text_path.setObjectName("text_path")
        self.gridLayout.addWidget(self.text_path, 2, 1, 1, 1)
        self.text_base = QtWidgets.QLineEdit(self.api_group)
        self.text_base.setObjectName("text_base")
        self.gridLayout.addWidget(self.text_base, 1, 1, 1, 1)
        self.text_name = QtWidgets.QLineEdit(self.api_group)
        self.text_name.setObjectName("text_name")
        self.gridLayout.addWidget(self.text_name, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.api_group)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.api_group)
        self.verticalLayout.addWidget(self.key_group)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.key_text, self.text_base)
        Dialog.setTabOrder(self.text_base, self.text_path)
        Dialog.setTabOrder(self.text_path, self.text_name)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.key_group.setTitle(_translate("Dialog", "API key"))
        self.api_group.setTitle(_translate("Dialog", "URL"))
        self.label_2.setText(_translate("Dialog", "Path"))
        self.label.setText(_translate("Dialog", "Base"))
        self.label_3.setText(_translate("Dialog", "Name"))

