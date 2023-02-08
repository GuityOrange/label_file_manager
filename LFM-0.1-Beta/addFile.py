# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list_view.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class QTreeWidget_(QtWidgets.QTreeWidget):
    itemRightClicked = pyqtSignal()

    def itemClicked(self, evt):
        super().itemClicked(evt)
        # 为右键单击事件建立信号
        if evt.button() == Qt.RightButton:
            self.itemRightClicked.emit()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(609, 542)
        Form.setMinimumSize(QtCore.QSize(609, 542))
        Form.setMaximumSize(QtCore.QSize(609, 542))
        self.label_treeWidget = QTreeWidget_(Form)
        self.label_treeWidget.setGeometry(QtCore.QRect(10, 10, 301, 521))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_treeWidget.setFont(font)
        self.label_treeWidget.setObjectName("label_treeWidget")
        self.add_pushButton = QtWidgets.QPushButton(Form)
        self.add_pushButton.setGeometry(QtCore.QRect(470, 20, 121, 31))
        self.add_pushButton.setObjectName("add_pushButton")
        self.label_pushButton = QtWidgets.QPushButton(Form)
        self.label_pushButton.setGeometry(QtCore.QRect(500, 70, 91, 31))
        self.label_pushButton.setObjectName("label_pushButton")
        self.label_lineEdit = QtWidgets.QLineEdit(Form)
        self.label_lineEdit.setGeometry(QtCore.QRect(330, 70, 151, 31))
        self.label_lineEdit.setObjectName("label_lineEdit")
        self.selected_listWidget = QtWidgets.QListWidget(Form)
        self.selected_listWidget.setGeometry(QtCore.QRect(330, 160, 256, 192))
        self.selected_listWidget.setObjectName("selected_listWidget")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(330, 125, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.feedback = QtWidgets.QTextBrowser(Form)
        self.feedback.setGeometry(QtCore.QRect(330, 370, 261, 161))
        self.feedback.setObjectName("feedback")
        self.delete_pushButton = QtWidgets.QPushButton(Form)
        self.delete_pushButton.setGeometry(QtCore.QRect(500, 120, 91, 31))
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.help_pushButton = QtWidgets.QPushButton(Form)
        self.help_pushButton.setGeometry(QtCore.QRect(330, 20, 121, 31))
        self.help_pushButton.setObjectName("help_pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_treeWidget.headerItem().setText(0, _translate("Form", "标签树"))
        self.add_pushButton.setText(_translate("Form", "添加至仓库"))
        self.label_pushButton.setText(_translate("Form", "添加标签"))
        self.label.setText(_translate("Form", "已经选择的标签"))
        self.delete_pushButton.setText(_translate("Form", "删除标签"))
        self.help_pushButton.setText(_translate("Form", "帮助"))

