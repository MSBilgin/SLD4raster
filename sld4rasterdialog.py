# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sld4raster 
                                 A QGIS plugin
 QGIS 2 plugin to generate SLD (Styled Layer Descriptor) for raster layers. 
 Also it can transform SLD documents to QGIS Layer Style File (*.qgs).
 It supports multiband, singleband pseudocolor, gradient (white to black, black to white) styles also color interpolation type and opacity levels.
                             -------------------
        begin                : 2014-02-06
		version				 : 0.8
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

from PyQt4 import QtCore, QtGui
from ui_sld4raster import Ui_sld4raster
from qgis.core import *
# create the dialog for zoom to point


class sld4rasterDialog(QtGui.QDialog, Ui_sld4raster):
        def __init__(self):
                QtGui.QMainWindow.__init__(self)
                self.setupUi(self) 
				
