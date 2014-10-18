# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sld4raster 
                                 A QGIS plugin
 QGIS 2 plugin to generate SLD (Styled Layer Descriptor) for raster layers. 
 It can transform SLD documents to QGIS Layer Style File (*.qgs).
 Supports multiband, singleband pseudocolor, gradient (white to black, black to white) styles also color interpolation type and opacity levels.
 Integrated with GeoServer Rest API. Provides direct upload of the styles.
                             -------------------
        begin                : 2014-10-09
		version				 : 0.9
        copyright            : (C) 2014 by Mehmet Selim BILGIN
        email                : mselimbilgin@yahoo.com
		web					 : http://cbsuygulama.wordpress.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui, uic
import os

MainFormClass, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_sld4raster.ui'))

UploadFormClass, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_gsUpload.ui'))

class sld4rasterDialog(QtGui.QDialog, MainFormClass):
		def __init__(self):
			QtGui.QDialog.__init__(self)
			self.setupUi(self)
				
class gsUploadDialog(QtGui.QDialog, UploadFormClass):
		def __init__(self):
			QtGui.QDialog.__init__(self)
			self.setupUi(self)
				
