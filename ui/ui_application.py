# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'application.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(795, 695)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.splitter_2 = QtWidgets.QSplitter(self.centralWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.portCBox = QtWidgets.QComboBox(self.widget)
        self.portCBox.setObjectName("portCBox")
        self.horizontalLayout.addWidget(self.portCBox)
        self.baudCBox = QtWidgets.QComboBox(self.widget)
        self.baudCBox.setObjectName("baudCBox")
        self.horizontalLayout.addWidget(self.baudCBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectButton = QtWidgets.QPushButton(self.widget)
        self.connectButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)
        self.versionLabel = QtWidgets.QLabel(self.widget)
        self.versionLabel.setText("")
        self.versionLabel.setObjectName("versionLabel")
        self.horizontalLayout.addWidget(self.versionLabel)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.actionList = QtWidgets.QListWidget(self.widget)
        self.actionList.setObjectName("actionList")
        self.horizontalLayout_2.addWidget(self.actionList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.upActionButton = QtWidgets.QPushButton(self.widget)
        self.upActionButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.upActionButton.setObjectName("upActionButton")
        self.verticalLayout.addWidget(self.upActionButton)
        self.downActionButton = QtWidgets.QPushButton(self.widget)
        self.downActionButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.downActionButton.setObjectName("downActionButton")
        self.verticalLayout.addWidget(self.downActionButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.addActionButton = QtWidgets.QPushButton(self.widget)
        self.addActionButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.addActionButton.setObjectName("addActionButton")
        self.horizontalLayout_5.addWidget(self.addActionButton)
        self.removeActionButton = QtWidgets.QPushButton(self.widget)
        self.removeActionButton.setMaximumSize(QtCore.QSize(70, 16777215))
        self.removeActionButton.setObjectName("removeActionButton")
        self.horizontalLayout_5.addWidget(self.removeActionButton)
        self.editActionButton = QtWidgets.QPushButton(self.widget)
        self.editActionButton.setMaximumSize(QtCore.QSize(45, 16777215))
        self.editActionButton.setObjectName("editActionButton")
        self.horizontalLayout_5.addWidget(self.editActionButton)
        spacerItem2 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.filterList = QtWidgets.QListWidget(self.widget1)
        self.filterList.setObjectName("filterList")
        self.horizontalLayout_6.addWidget(self.filterList)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.upFilterButton = QtWidgets.QPushButton(self.widget1)
        self.upFilterButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.upFilterButton.setObjectName("upFilterButton")
        self.verticalLayout_3.addWidget(self.upFilterButton)
        self.downFilterButton = QtWidgets.QPushButton(self.widget1)
        self.downFilterButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.downFilterButton.setObjectName("downFilterButton")
        self.verticalLayout_3.addWidget(self.downFilterButton)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addFilterButton = QtWidgets.QPushButton(self.widget1)
        self.addFilterButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.addFilterButton.setObjectName("addFilterButton")
        self.horizontalLayout_4.addWidget(self.addFilterButton)
        self.removeFilterButton = QtWidgets.QPushButton(self.widget1)
        self.removeFilterButton.setMaximumSize(QtCore.QSize(70, 16777215))
        self.removeFilterButton.setObjectName("removeFilterButton")
        self.horizontalLayout_4.addWidget(self.removeFilterButton)
        self.editFilterButton = QtWidgets.QPushButton(self.widget1)
        self.editFilterButton.setMaximumSize(QtCore.QSize(45, 16777215))
        self.editFilterButton.setObjectName("editFilterButton")
        self.horizontalLayout_4.addWidget(self.editFilterButton)
        spacerItem4 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.clearButton = QtWidgets.QPushButton(self.layoutWidget)
        self.clearButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.clearButton.setObjectName("clearButton")
        self.verticalLayout_2.addWidget(self.clearButton)
        self.comActivityEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.comActivityEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.comActivityEdit.setObjectName("comActivityEdit")
        self.verticalLayout_2.addWidget(self.comActivityEdit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sendLabel = QtWidgets.QLabel(self.layoutWidget)
        self.sendLabel.setObjectName("sendLabel")
        self.horizontalLayout_3.addWidget(self.sendLabel)
        self.sendLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.sendLineEdit.setObjectName("sendLineEdit")
        self.horizontalLayout_3.addWidget(self.sendLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.action_Save_com_port = QtWidgets.QAction(MainWindow)
        self.action_Save_com_port.setObjectName("action_Save_com_port")
        self.actionSave_Actions = QtWidgets.QAction(MainWindow)
        self.actionSave_Actions.setObjectName("actionSave_Actions")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fast Serial"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.upActionButton.setText(_translate("MainWindow", "Up"))
        self.downActionButton.setText(_translate("MainWindow", "Dn"))
        self.addActionButton.setText(_translate("MainWindow", "Add"))
        self.removeActionButton.setText(_translate("MainWindow", "Remove"))
        self.editActionButton.setText(_translate("MainWindow", "Edit"))
        self.upFilterButton.setText(_translate("MainWindow", "Up"))
        self.downFilterButton.setText(_translate("MainWindow", "Dn"))
        self.addFilterButton.setText(_translate("MainWindow", "Add"))
        self.removeFilterButton.setText(_translate("MainWindow", "Remove"))
        self.editFilterButton.setText(_translate("MainWindow", "Edit"))
        self.clearButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Run selected tests.</p></body></html>"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.sendLabel.setText(_translate("MainWindow", "Send:"))
        self.action_Save_com_port.setText(_translate("MainWindow", "&Save Com Port"))
        self.actionSave_Actions.setText(_translate("MainWindow", "Save &Actions"))
