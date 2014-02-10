# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sld4raster.ui'
#
#        copyright            : (C) 2014 by M. Selim Bilgin
#        email                : mselimbilgin@yahoo.com
#		 web				  : http://cbsuygulama.wordpress.com
# 		 Created: Mon Feb 10 01:10:45 2014
#     	 by: PyQt4 UI code generator 4.10.3
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
        sld4raster.setFixedSize(561, 502)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sld4raster.sizePolicy().hasHeightForWidth())
        sld4raster.setSizePolicy(sizePolicy)
        self.comboBox = QtGui.QComboBox(sld4raster)
        self.comboBox.setGeometry(QtCore.QRect(30, 70, 361, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.generateBtn = QtGui.QPushButton(sld4raster)
        self.generateBtn.setGeometry(QtCore.QRect(430, 70, 101, 23))
        self.generateBtn.setObjectName(_fromUtf8("generateBtn"))
        self.textEdit = QtGui.QTextEdit(sld4raster)
        self.textEdit.setGeometry(QtCore.QRect(30, 120, 501, 311))
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.saveBtn = QtGui.QPushButton(sld4raster)
        self.saveBtn.setGeometry(QtCore.QRect(430, 460, 101, 23))
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.label = QtGui.QLabel(sld4raster)
        self.label.setGeometry(QtCore.QRect(30, 40, 71, 21))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(sld4raster)
        QtCore.QMetaObject.connectSlotsByName(sld4raster)

    def retranslateUi(self, sld4raster):
        sld4raster.setWindowTitle(_translate("sld4raster", "SLD4raster", None))
        self.generateBtn.setText(_translate("sld4raster", "Generate SLD", None))
        self.saveBtn.setText(_translate("sld4raster", "Save file...", None))
        self.label.setText(_translate("sld4raster", "Raster Layer", None))

