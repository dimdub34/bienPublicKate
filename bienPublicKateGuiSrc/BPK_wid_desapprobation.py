# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BPK_wid_desapprobation.ui'
#
# Created: Wed Jun  8 13:15:22 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(538, 78)
        self.verticalLayout_5 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_compte = QtGui.QLabel(Form)
        self.label_compte.setObjectName(_fromUtf8("label_compte"))
        self.verticalLayout.addWidget(self.label_compte)
        self.label_desapprobation = QtGui.QLabel(Form)
        self.label_desapprobation.setObjectName(_fromUtf8("label_desapprobation"))
        self.verticalLayout.addWidget(self.label_desapprobation)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.spinBox_0 = QtGui.QSpinBox(Form)
        self.spinBox_0.setReadOnly(True)
        self.spinBox_0.setObjectName(_fromUtf8("spinBox_0"))
        self.verticalLayout_2.addWidget(self.spinBox_0)
        self.spinBox_des_0 = QtGui.QSpinBox(Form)
        self.spinBox_des_0.setObjectName(_fromUtf8("spinBox_des_0"))
        self.verticalLayout_2.addWidget(self.spinBox_des_0)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.spinBox_1 = QtGui.QSpinBox(Form)
        self.spinBox_1.setReadOnly(True)
        self.spinBox_1.setObjectName(_fromUtf8("spinBox_1"))
        self.verticalLayout_3.addWidget(self.spinBox_1)
        self.spinBox_des_1 = QtGui.QSpinBox(Form)
        self.spinBox_des_1.setObjectName(_fromUtf8("spinBox_des_1"))
        self.verticalLayout_3.addWidget(self.spinBox_des_1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.spinBox_2 = QtGui.QSpinBox(Form)
        self.spinBox_2.setReadOnly(True)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.verticalLayout_4.addWidget(self.spinBox_2)
        self.spinBox_des_2 = QtGui.QSpinBox(Form)
        self.spinBox_des_2.setObjectName(_fromUtf8("spinBox_des_2"))
        self.verticalLayout_4.addWidget(self.spinBox_des_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_compte.setText(_translate("Form", "Compte collectif", None))
        self.label_desapprobation.setText(_translate("Form", "Points de désapprobation", None))

