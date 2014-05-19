# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sld4raster.ui'
#
# QGIS 2 plugin to generate SLD (Styled Layer Descriptor) for raster layers. Also it can transform SLD documents to QGIS Layer Style File (*.qgs). It supports multiband, singleband pseudocolor, gradient (white to black, black to white) styles also color interpolation type and opacity levels.
#        begin                : 2014-02-06
#		 version			  : 0.8
#        copyright            : (C) 2014 by Mehmet Selim BILGIN
#        email                : mselimbilgin@yahoo.com
#		 web				  : http://cbsuygulama.wordpress.com
# Created: Sun May 18 17:57:43 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_sld4raster(object):
    def setupUi(self, sld4raster):
        sld4raster.setObjectName(_fromUtf8("sld4raster"))
        sld4raster.setFixedSize(541, 558)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sld4raster.sizePolicy().hasHeightForWidth())
        sld4raster.setSizePolicy(sizePolicy)
        sld4raster.setStyleSheet(_fromUtf8(""))
        self.tabWidget = QtGui.QTabWidget(sld4raster)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 543, 560))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(_fromUtf8("QTabBar::tab { min-width: 270px; min-height: 30px;}"))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setGeometry(QtCore.QRect(20, 70, 361, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.textEdit = QtGui.QTextEdit(self.tab)
        self.textEdit.setGeometry(QtCore.QRect(20, 120, 501, 331))
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.generateBtn = QtGui.QPushButton(self.tab)
        self.generateBtn.setGeometry(QtCore.QRect(420, 70, 101, 23))
        self.generateBtn.setObjectName(_fromUtf8("generateBtn"))
        self.saveBtn = QtGui.QPushButton(self.tab)
        self.saveBtn.setGeometry(QtCore.QRect(420, 480, 101, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.saveBtn.setFont(font)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.validateBtn = QtGui.QPushButton(self.tab)
        self.validateBtn.setGeometry(QtCore.QRect(20, 460, 75, 23))
        self.validateBtn.setObjectName(_fromUtf8("validateBtn"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.textEdit_2 = QtGui.QTextEdit(self.tab_2)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 120, 501, 331))
        self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.translateBtn = QtGui.QPushButton(self.tab_2)
        self.translateBtn.setGeometry(QtCore.QRect(380, 480, 141, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.translateBtn.setFont(font)
        self.translateBtn.setObjectName(_fromUtf8("translateBtn"))
        self.browseBtn = QtGui.QPushButton(self.tab_2)
        self.browseBtn.setGeometry(QtCore.QRect(440, 70, 81, 23))
        self.browseBtn.setObjectName(_fromUtf8("browseBtn"))
        self.lineEdit = QtGui.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(20, 70, 381, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.validateBtn_2 = QtGui.QPushButton(self.tab_2)
        self.validateBtn_2.setGeometry(QtCore.QRect(20, 460, 75, 23))
        self.validateBtn_2.setObjectName(_fromUtf8("validateBtn_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(sld4raster)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(sld4raster)

    def retranslateUi(self, sld4raster):
        sld4raster.setWindowTitle(_translate("sld4raster", "SLD4raster", None))
        self.label.setText(_translate("sld4raster", "Raster Layer", None))
        self.generateBtn.setText(_translate("sld4raster", "Generate SLD", None))
        self.saveBtn.setText(_translate("sld4raster", "Save file...", None))
        self.validateBtn.setText(_translate("sld4raster", "Validate ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("sld4raster", "Generate SLD Document", None))
        self.translateBtn.setText(_translate("sld4raster", "Translate to QGS file...", None))
        self.browseBtn.setText(_translate("sld4raster", "Browse...", None))
        self.label_2.setText(_translate("sld4raster", "Input SLD File", None))
        self.validateBtn_2.setText(_translate("sld4raster", "Validate ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("sld4raster", "Transform SLD Document", None))

