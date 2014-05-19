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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load sld4raster class from file sld4raster
    from sld4raster import sld4raster
    return sld4raster(iface)