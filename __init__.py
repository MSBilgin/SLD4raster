# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sld4raster
                                 A QGIS plugin
 QGIS 2 plugin to generate SLD (Styled Layer Descriptor) for raster layers. It supports multiband, singleband pseudocolor, gradient (white to black, black to white) styles also color interpolation and opacity levels.
                             -------------------
        begin                : 2014-02-06
        copyright            : (C) 2014 by M. Selim Bilgin
        email                : mselimbilgin@yahoo.com
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
