# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rename.ui'
#
# Created: Sun Mar 13 23:53:14 2016
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
        Dialog.resize(502, 363)
        Dialog.setSizeGripEnabled(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ChooseFileBtn = QtGui.QPushButton(Dialog)
        self.ChooseFileBtn.setObjectName(_fromUtf8("ChooseFileBtn"))
        self.horizontalLayout.addWidget(self.ChooseFileBtn)
        self.RenameBtn = QtGui.QPushButton(Dialog)
        self.RenameBtn.setObjectName(_fromUtf8("RenameBtn"))
        self.horizontalLayout.addWidget(self.RenameBtn)
        self.ExportInfoBtn = QtGui.QPushButton(Dialog)
        self.ExportInfoBtn.setObjectName(_fromUtf8("ExportInfoBtn"))
        self.horizontalLayout.addWidget(self.ExportInfoBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.FileListView = QtGui.QListView(Dialog)
        self.FileListView.setObjectName(_fromUtf8("FileListView"))
        self.verticalLayout.addWidget(self.FileListView)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ChooseFileBtn.setText(_translate("Dialog", "&Choose Files", None))
        self.RenameBtn.setText(_translate("Dialog", "&Rename", None))
        self.ExportInfoBtn.setText(_translate("Dialog", "&Export Info", None))

