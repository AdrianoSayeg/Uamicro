# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P1.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(766, 490)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(180, 10, 351, 27))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_archivos = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_archivos.setObjectName("pushButton_archivos")
        self.horizontalLayout.addWidget(self.pushButton_archivos)
        self.pushButton_modificar = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_modificar.setObjectName("pushButton_modificar")
        self.horizontalLayout.addWidget(self.pushButton_modificar)
        self.pushButton_ejecutar = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_ejecutar.setObjectName("pushButton_ejecutar")
        self.horizontalLayout.addWidget(self.pushButton_ejecutar)
        self.pushButton_modo = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_modo.setObjectName("pushButton_modo")
        self.horizontalLayout.addWidget(self.pushButton_modo)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(140, 320, 218, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.label_busc_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_busc_2.setObjectName("label_busc_2")
        self.horizontalLayout_5.addWidget(self.label_busc_2)
        self.layoutWidget2 = QtWidgets.QWidget(Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 70, 301, 217))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_14 = QtWidgets.QLabel(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget2)
        self.tableWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.layoutWidget3 = QtWidgets.QWidget(Form)
        self.layoutWidget3.setGeometry(QtCore.QRect(310, 80, 261, 196))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_busd = QtWidgets.QLabel(self.layoutWidget3)
        self.label_busd.setObjectName("label_busd")
        self.gridLayout_2.addWidget(self.label_busd, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget3)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_OUT = QtWidgets.QLabel(self.layoutWidget3)
        self.label_OUT.setObjectName("label_OUT")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_OUT)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_A = QtWidgets.QLabel(self.layoutWidget3)
        self.label_A.setObjectName("label_A")
        self.horizontalLayout_2.addWidget(self.label_A)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.label_ALU = QtWidgets.QLabel(self.layoutWidget3)
        self.label_ALU.setObjectName("label_ALU")
        self.horizontalLayout_4.addWidget(self.label_ALU)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 3, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_B = QtWidgets.QLabel(self.layoutWidget3)
        self.label_B.setObjectName("label_B")
        self.horizontalLayout_3.addWidget(self.label_B)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 4, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.label_PC = QtWidgets.QLabel(self.layoutWidget3)
        self.label_PC.setObjectName("label_PC")
        self.horizontalLayout_6.addWidget(self.label_PC)
        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 3, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.label_AR = QtWidgets.QLabel(self.layoutWidget3)
        self.label_AR.setObjectName("label_AR")
        self.horizontalLayout_7.addWidget(self.label_AR)
        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 3, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_15 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_8.addWidget(self.label_15)
        self.label_IR = QtWidgets.QLabel(self.layoutWidget3)
        self.label_IR.setObjectName("label_IR")
        self.horizontalLayout_8.addWidget(self.label_IR)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 3, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_busc = QtWidgets.QLabel(self.layoutWidget3)
        self.label_busc.setObjectName("label_busc")
        self.gridLayout_3.addWidget(self.label_busc, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_archivos.setText(_translate("Form", "ARCHIVOS"))
        self.pushButton_modificar.setText(_translate("Form", "MODIFICAR"))
        self.pushButton_ejecutar.setText(_translate("Form", "EJECUTAR"))
        self.pushButton_modo.setText(_translate("Form", "MODO"))
        self.label_9.setText(_translate("Form", "MODO"))
        self.label_busc_2.setText(_translate("Form", "CONTINUA"))
        self.label_14.setText(_translate("Form", "MEMORIA"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "dir"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "dato"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "inst"))
        self.label_12.setText(_translate("Form", "ARQUITECTURA"))
        self.label_8.setText(_translate("Form", "BUS DE DATOSY DIRECCIONES"))
        self.label_busd.setText(_translate("Form", "00"))
        self.label.setText(_translate("Form", "OUT"))
        self.label_OUT.setText(_translate("Form", "00"))
        self.label_3.setText(_translate("Form", "MEM"))
        self.label_2.setText(_translate("Form", "A"))
        self.label_A.setText(_translate("Form", "00"))
        self.label_7.setText(_translate("Form", "ALU"))
        self.label_ALU.setText(_translate("Form", "00"))
        self.label_5.setText(_translate("Form", "B"))
        self.label_B.setText(_translate("Form", "00"))
        self.label_11.setText(_translate("Form", "PC"))
        self.label_PC.setText(_translate("Form", "00"))
        self.label_13.setText(_translate("Form", "AR"))
        self.label_AR.setText(_translate("Form", "00"))
        self.label_15.setText(_translate("Form", "IR"))
        self.label_IR.setText(_translate("Form", "00"))
        self.label_4.setText(_translate("Form", "CONTROL"))
        self.label_6.setText(_translate("Form", "BUS DE CONTROL"))
        self.label_busc.setText(_translate("Form", "00"))
