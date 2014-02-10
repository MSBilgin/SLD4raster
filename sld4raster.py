# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sld4raster
                                 A QGIS plugin
 QGIS 2 plugin to generate SLD (Styled Layer Descriptor) for raster layers. It supports multiband style (with different band order), singleband pseudocolor, gradient (white to black, black to white) styles also color interpolation and opacity levels.
                              -------------------
        begin                : 2014-02-06
        copyright            : (C) 2014 by M. Selim Bilgin
        email                : mselimbilgin@yahoo.com
		web				  	 : http://cbsuygulama.wordpress.com
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources_rc
from sld4rasterdialog import sld4rasterDialog

from PyQt4.QtXml import QDomDocument
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class sld4raster:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/sld4raster/icon.png"),
            u"SLD4raster", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&SLD4raster", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&SLD4raster", self.action)
        self.iface.removeToolBarIcon(self.action)	

    def saveFile(self):
	saveDlg = QFileDialog.getSaveFileName(self.dlg, "Save SLD File...",".", "SLD File (*.sld)")
	if saveDlg:
            try:
                with open(saveDlg, 'w') as sldFile:
                    sldFile.write(self.dlg.textEdit.toPlainText())
                QMessageBox.information(None, "Information", "The SLD file has been succesfully saved.")
            except Exception as saveError:
                QMessageBox.critical(None, "Information", ("An error has occured: " + str(saveError)))		

    def noRasterLayer(self):
        QMessageBox.critical(None, "Information", "There is no raster layer in QGIS canvas.")
        
    
    def sldMake(self):
        for (i,j) in self.allMapLayers:
            if j.name() == self.dlg.comboBox.currentText():
		ourRasterLayer = j
		break
	qmlDocument = QDomDocument()
	root = qmlDocument.createElement('SLD4raster')
	qmlDocument.appendChild(root)
	qgisNode = qmlDocument.createElement('qgis')
	root.appendChild(qgisNode)
	#I got error with importing QString class. So i found this solution.
	QString = str
	errMessage = QString("")
	ourRasterLayer.writeSymbology(qgisNode, qmlDocument, errMessage)
				
	qmlString = minidom.parseString(qmlDocument.toString())

        sldRoot = Element('sld:StyledLayerDescriptor')
	sldRoot.attrib['xmlns'] = 'http://www.opengis.net/sld'
	sldRoot.attrib['xmlns:sld'] = 'http://www.opengis.net/sld'
	sldRoot.attrib['xmlns:ogc'] = 'http://www.opengis.net/ogc'
	sldRoot.attrib['xmlns:gml'] = 'http://www.opengis.net/gml'
	sldRoot.attrib['version'] = '1.0.0'
        	        
        userLayer = SubElement(sldRoot, 'sld:UserLayer')
	layerFeatureConstraints = SubElement(userLayer, 'sld:LayerFeatureConstraints')
        featureTypeConstraint  = SubElement (layerFeatureConstraints, 'sld:FeatureTypeConstraint')
	userStyle = SubElement(userLayer, 'sld:UserStyle')
	styleName = SubElement(userStyle, 'sld:Name')
	styleName.text = self.dlg.comboBox.currentText()
	styleTitle = SubElement(userStyle, 'sld:Title')
	featureTypeStyle = SubElement(userStyle, 'sld:FeatureTypeStyle')
	featureName = SubElement(featureTypeStyle, 'sld:Name')
	featureRule = SubElement(featureTypeStyle, 'sld:Rule')
	rasterSymbolizer = SubElement(featureRule, 'sld:RasterSymbolizer')
	geometry = SubElement(rasterSymbolizer, 'sld:Geometry')
	ogcPropertyName = SubElement(geometry, 'ogc:PropertyName')
	ogcPropertyName.text = 'grid'
	opacity = SubElement(rasterSymbolizer, 'sld:Opacity')

        ###Getting raster type parameters
	rasterType = str(qmlString.getElementsByTagName('rasterrenderer')[0].attributes['type'].value)
	isGradient = qmlString.getElementsByTagName('rasterrenderer')[0].attributes.has_key('gradient') 

        ###SLD for multiband raster
	if rasterType == 'multibandcolor':
	    ###Getting RGB band order.
	    redBand = str(qmlString.getElementsByTagName('rasterrenderer')[0].attributes['redBand'].value)
            greenBand = str(qmlString.getElementsByTagName('rasterrenderer')[0].attributes['greenBand'].value)
            blueBand = str(qmlString.getElementsByTagName('rasterrenderer')[0].attributes['blueBand'].value)
			
	    channelSelection = SubElement(rasterSymbolizer, 'sld:ChannelSelection')
			
	    redChannel = SubElement(channelSelection, 'sld:RedChannel')
	    redSourceChannel = SubElement(redChannel, 'sld:SourceChannelName')
	    redSourceChannel.text = redBand
			
	    greenChannel = SubElement(channelSelection, 'sld:GreenChannel')
	    greenSourceChannel = SubElement(greenChannel, 'sld:SourceChannelName')
	    greenSourceChannel.text = greenBand
			
	    blueChannel = SubElement(channelSelection, 'sld:BlueChannel')
	    blueSourceChannel = SubElement(blueChannel, 'sld:SourceChannelName')
            blueSourceChannel.text = blueBand
            
	###SLD for gradiented (black to white) raster
	elif isGradient:
            blackWhiteColor = ['#000000','#FFFFFF']
	    colorMap = SubElement(rasterSymbolizer, 'sld:ColorMap')
	    gradientType = qmlString.getElementsByTagName('rasterrenderer')[0].attributes['gradient'].value
	    blackWhiteValue = [qmlString.getElementsByTagName('minValue')[0].firstChild.nodeValue, qmlString.getElementsByTagName('maxValue')[0].firstChild.nodeValue]

        ###Getting gradient color type
            if gradientType == 'WhiteToBlack':
                blackWhiteColor.reverse()

            for i in range(len(blackWhiteColor)):
                colorMapEntry = SubElement(colorMap, 'sld:ColorMapEntry')
		colorMapEntry.attrib['color'] = blackWhiteColor[i]
		colorMapEntry.attrib['opacity'] = '1.0'
		colorMapEntry.attrib['quantity'] = blackWhiteValue[i]

        ###SLD for singleband raster
        else:
            colorMap = SubElement(rasterSymbolizer, 'sld:ColorMap')

            ###Getting color ramp type
            colorType = str(qmlString.getElementsByTagName('colorrampshader')[0].attributes['colorRampType'].value)
            if colorType == 'DISCRETE':
                colorMap.attrib['type'] = "intervals"

            ###Getting color values
            colorValue = list()
            itemlist = qmlString.getElementsByTagName('item')
            for n in itemlist:
                colorValue.append([n.attributes['color'].value,n.attributes['value'].value])

            ###Color values posting to SLD document
            for i in range(len(colorValue)):
                colorMapEntry = SubElement(colorMap, 'sld:ColorMapEntry')
                colorMapEntry.attrib['color'] = colorValue[i][0].upper()
                colorMapEntry.attrib['opacity'] = '1.0'
                colorMapEntry.attrib['quantity'] = colorValue[i][1].upper()

        rasterOpacity = str(qmlString.getElementsByTagName('rasterrenderer')[0].attributes['opacity'].value)
        opacity.text = rasterOpacity
        textXML = minidom.parseString(tostring(sldRoot))
        self.dlg.textEdit.setText(textXML.toprettyxml(indent = "    "))

            
    def run(self):
	self.dlg = sld4rasterDialog()
	self.dlg.generateBtn.clicked.connect(self.sldMake)
	self.dlg.saveBtn.clicked.connect(self.saveFile)
			
	self.allMapLayers = QgsMapLayerRegistry.instance().mapLayers().items()
		
	for (notImportantForNow, layerObj) in self.allMapLayers:
            if layerObj.type() == QgsMapLayer.RasterLayer:
		self.dlg.comboBox.addItem(layerObj.name())

	if self.dlg.comboBox.count() == 0:
            self.dlg.generateBtn.clicked.disconnect(self.sldMake)
            self.dlg.generateBtn.clicked.connect(self.noRasterLayer)

        self.dlg.exec_()  #By using exec_() function the plugin window will be top most and QGIS window deactivated.
