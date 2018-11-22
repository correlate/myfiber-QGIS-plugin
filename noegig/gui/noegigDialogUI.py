# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/noegigDialogUI.ui'
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
        self.verticalLayout.addWidget(self.key_group)
        self.api_group = QtWidgets.QGroupBox(Dialog)
        self.api_group.setObjectName("api_group")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.api_group)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sites_radio = QtWidgets.QRadioButton(self.api_group)
        self.sites_radio.setObjectName("sites_radio")
        self.verticalLayout_3.addWidget(self.sites_radio)
        self.locations_radio = QtWidgets.QRadioButton(self.api_group)
        self.locations_radio.setObjectName("locations_radio")
        self.verticalLayout_3.addWidget(self.locations_radio)
        self.regions_radio = QtWidgets.QRadioButton(self.api_group)
        self.regions_radio.setObjectName("regions_radio")
        self.verticalLayout_3.addWidget(self.regions_radio)
        self.verticalLayout.addWidget(self.api_group)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.key_group.setTitle(_translate("Dialog", "API key"))
        self.api_group.setTitle(_translate("Dialog", "APIs"))
        self.sites_radio.setText(_translate("Dialog", "Query sites"))
        self.locations_radio.setText(_translate("Dialog", "Query locations"))
        self.regions_radio.setText(_translate("Dialog", "Query regions"))

