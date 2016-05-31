# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bienPublicKateGuiSrcDesapprobation.ui'
#
# Created: Tue Mar 31 14:43:02 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(538, 493)
        self.verticalLayout_5 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_periode = QtGui.QLabel(Dialog)
        self.label_periode.setObjectName(_fromUtf8("label_periode"))
        self.horizontalLayout.addWidget(self.label_periode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_historique = QtGui.QPushButton(Dialog)
        self.pushButton_historique.setObjectName(_fromUtf8("pushButton_historique"))
        self.horizontalLayout.addWidget(self.pushButton_historique)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.textEdit_explication = QtGui.QTextEdit(Dialog)
        self.textEdit_explication.setMaximumSize(QtCore.QSize(16777214, 16777214))
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.horizontalLayout_2.addWidget(self.textEdit_explication)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.spinBox_0 = QtGui.QSpinBox(Dialog)
        self.spinBox_0.setReadOnly(True)
        self.spinBox_0.setObjectName(_fromUtf8("spinBox_0"))
        self.verticalLayout_2.addWidget(self.spinBox_0)
        self.spinBox_des_0 = QtGui.QSpinBox(Dialog)
        self.spinBox_des_0.setObjectName(_fromUtf8("spinBox_des_0"))
        self.verticalLayout_2.addWidget(self.spinBox_des_0)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.spinBox_1 = QtGui.QSpinBox(Dialog)
        self.spinBox_1.setReadOnly(True)
        self.spinBox_1.setObjectName(_fromUtf8("spinBox_1"))
        self.verticalLayout_3.addWidget(self.spinBox_1)
        self.spinBox_des_1 = QtGui.QSpinBox(Dialog)
        self.spinBox_des_1.setObjectName(_fromUtf8("spinBox_des_1"))
        self.verticalLayout_3.addWidget(self.spinBox_des_1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.spinBox_2 = QtGui.QSpinBox(Dialog)
        self.spinBox_2.setReadOnly(True)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.verticalLayout_4.addWidget(self.spinBox_2)
        self.spinBox_des_2 = QtGui.QSpinBox(Dialog)
        self.spinBox_des_2.setObjectName(_fromUtf8("spinBox_des_2"))
        self.verticalLayout_4.addWidget(self.spinBox_des_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem10)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_5.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.spinBox_des_0, self.spinBox_des_1)
        Dialog.setTabOrder(self.spinBox_des_1, self.spinBox_des_2)
        Dialog.setTabOrder(self.spinBox_des_2, self.buttonBox)
        Dialog.setTabOrder(self.buttonBox, self.pushButton_historique)
        Dialog.setTabOrder(self.pushButton_historique, self.textEdit_explication)
        Dialog.setTabOrder(self.textEdit_explication, self.spinBox_0)
        Dialog.setTabOrder(self.spinBox_0, self.spinBox_1)
        Dialog.setTabOrder(self.spinBox_1, self.spinBox_2)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_periode.setText(_translate("Dialog", "TextLabel", None))
        self.pushButton_historique.setText(_translate("Dialog", "Historique", None))
        self.label.setText(_translate("Dialog", "Compte collectif", None))
        self.label_2.setText(_translate("Dialog", "Points de désapprobation", None))

