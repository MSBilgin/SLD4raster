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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources_rc
from sld4rasterdialog import sld4rasterDialog

from PyQt4.QtXml import QDomDocument
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import codecs

class sld4raster:
	def __init__(self, iface):
        # Save reference to the QGIS interface
		self.iface = iface
		
	def initGui(self):
        # Create action that will start plugin configuration
		self.action = QAction(QIcon(":/plugins/sld4raster/icon.png"), u"SLD4raster", self.iface.mainWindow())
 
        # connect the action to the run method
		self.action.triggered.connect(self.run)
		
		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu(u"&SLD4raster", self.action)
		
	def unload(self):
        # Remove the plugin menu item and icon
		self.iface.removePluginMenu(u"&SLD4raster", self.action)
		self.iface.removeToolBarIcon(self.action)
		
	def saveFile(self, document, type):
		if type=='SLD':
			saveDlg = QFileDialog.getSaveFileName(self.dlg, "Save SLD File...",".", "SLD file (*.sld);; XML file (*.xml)")
			saveMessage = "The SLD document has been succesfully saved."
		else:
			saveDlg = QFileDialog.getSaveFileName(self.dlg, "Save SLD File...",".", "QGIS Layer Style File (*.qml)")
			saveMessage = 'SLD document has been succesfully translated to QML style file.'
			
		if saveDlg:
			try:
				with open(saveDlg, 'w') as File:
					File.write(document.encode('utf-8'))#UTF encoding for non-ASCII chars.
				QMessageBox.information(None, "Information", saveMessage)
			except Exception as saveError:
				QMessageBox.critical(None, "Information", ("An error has occured: " + str(saveError)))
		
	def browseFile(self):
		browseDlg = QFileDialog.getOpenFileName(self.dlg, "Choose SLD File...",".", "SLD file (*.sld);; XML file (*.xml)")
		if browseDlg:
			self.dlg.lineEdit.setText(browseDlg)
			try:
				with codecs.open(browseDlg, encoding='utf-8', mode='r') as readFile:
					self.dlg.textEdit_2.setText(readFile.read())
			except Exception as readError:	
				QMessageBox.critical(None, "Information", ("An error has occured: " + str(readError)))
			
	def validation(self, inputXML):			
		try:
			minidom.parseString(inputXML.encode("utf-8")) #UTF encoding for non-ASCII chars.
			QMessageBox.information(None, "Information", "The XML document is well-formed.")
		except Exception as SLDerror:
			QMessageBox.critical(None, "Information", ("Invalid XML document: " + str(SLDerror)))
		
			
	def sldTransform(self):
		sldDocument = minidom.parseString(self.dlg.textEdit_2.toPlainText().encode('utf-8'))
		#main QML structure.
		qmlRoot = Element('qgis')
		pipe = SubElement(qmlRoot, 'pipe')
		
		rasterRenderer = SubElement(pipe, 'rasterrenderer')
		rasterTransparency = SubElement(rasterRenderer,'rasterTransparency')
		
		#checking document for containing ColorMap tag. If does, it is a single-band raster.
		sldRasterType = sldDocument.getElementsByTagName('sld:ColorMap') 
		if len(sldRasterType) == 0 :
			sldRedBand = sldDocument.getElementsByTagName('sld:RedChannel')[0].getElementsByTagName('sld:SourceChannelName')[0].firstChild.nodeValue
			sldGreenBand = sldDocument.getElementsByTagName('sld:GreenChannel')[0].getElementsByTagName('sld:SourceChannelName')[0].firstChild.nodeValue
			sldBlueBand = sldDocument.getElementsByTagName('sld:BlueChannel')[0].getElementsByTagName('sld:SourceChannelName')[0].firstChild.nodeValue
						
			rasterRenderer.attrib['type'] = 'multibandcolor'
			rasterRenderer.attrib['redBand'] = sldRedBand
			rasterRenderer.attrib['greenBand'] = sldGreenBand
			rasterRenderer.attrib['blueBand'] = sldBlueBand
						
		else:
			rasterRenderer.attrib['type'] = 'singlebandpseudocolor'
			rasterRenderer.attrib['band'] = '1'
			rasterShader = SubElement(rasterRenderer, 'rastershader')
			
			colorRampShader = SubElement(rasterShader, 'colorrampshader')
									
			try:
				sldColorMapType = sldDocument.getElementsByTagName('sld:ColorMap')[0].attributes.has_key('type') #sometimes "ColorMap" tag does not contain "type" attribute. This means it is a ramp color.
				sldColorMapType2 = sldDocument.getElementsByTagName('sld:ColorMap')[0].attributes['type'].value #or getting raster map colortype by "type" atribute.
			except:
				pass
				
			if sldColorMapType and sldColorMapType2 == 'intervals':
				colorRampShader.attrib['colorRampType'] = 'DISCRETE'
			else:
				colorRampShader.attrib['colorRampType'] = 'INTERPOLATED'
			
			sldColorValues = list()
			sldItemList = sldDocument.getElementsByTagName('sld:ColorMapEntry')
			
			#some SLD documents don't have 'label' attribute so the problem is handled by this way.
			try:
				for m in sldItemList:
					sldColorValues.append([m.attributes['quantity'].value, m.attributes['label'].value, m.attributes['color'].value])
			except:
				for m in sldItemList:
					sldColorValues.append([m.attributes['quantity'].value, m.attributes['quantity'].value, m.attributes['color'].value])
				
			for s in range(len(sldColorValues)):
				item = SubElement(colorRampShader, 'item')
				item.attrib['alpha'] = '255'
				item.attrib['value'] = sldColorValues[s][0]
				item.attrib['label'] = sldColorValues[s][1]
				item.attrib['color'] = sldColorValues[s][2]

		
		#some SLD documents don't have 'sld:Opacity' tag so the problem is handled by this way.
		try:
			sldOpacity = sldDocument.getElementsByTagName('sld:Opacity')[0].firstChild.nodeValue
		except:
			sldOpacity = '1'
			
		rasterRenderer.attrib['opacity'] = sldOpacity
		
		brightnessContrast = SubElement(pipe, 'brightnesscontrast')
		hueSaturation = SubElement(pipe, 'huesaturation')
		rasterResampler = SubElement(pipe, 'rasterresampler')
		blendMode = SubElement(qmlRoot,'blendMode')
		blendMode.text = '0'
		textQML = minidom.parseString(tostring(qmlRoot)).toprettyxml(indent = "    ")
		self.saveFile(textQML, 'QML')


		
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
				
		qmlString = minidom.parseString(qmlDocument.toString().encode('utf-8')) #for non ASCII labels.

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
				colorValue.append([n.attributes['color'].value, n.attributes['value'].value, n.attributes['label'].value])

			###Color values posting to SLD document
			for i in range(len(colorValue)):
				colorMapEntry = SubElement(colorMap, 'sld:ColorMapEntry')
				colorMapEntry.attrib['color'] = colorValue[i][0]
				colorMapEntry.attrib['quantity'] = colorValue[i][1]
				colorMapEntry.attrib['label'] = colorValue[i][2]
				colorMapEntry.attrib['opacity'] = '1.0'				
				
		rasterOpacity = str(qmlString.getElementsByTagName('rasterrenderer')[0].attributes['opacity'].value)
		opacity.text = rasterOpacity
		textSLD = minidom.parseString(tostring(sldRoot))
		self.dlg.textEdit.setText(textSLD.toprettyxml(indent = "    "))

	def run(self):
		self.dlg = sld4rasterDialog()
		self.dlg.generateBtn.clicked.connect(self.sldMake)
		self.dlg.translateBtn.clicked.connect(self.sldTransform)
		self.dlg.saveBtn.clicked.connect(lambda: self.saveFile(self.dlg.textEdit.toPlainText(), 'SLD'))
		self.dlg.browseBtn.clicked.connect(self.browseFile)
		self.dlg.validateBtn.clicked.connect(lambda: self.validation(self.dlg.textEdit.toPlainText()))
		self.dlg.validateBtn_2.clicked.connect(lambda: self.validation(self.dlg.textEdit_2.toPlainText()))
		self.allMapLayers = QgsMapLayerRegistry.instance().mapLayers().items()

		for (notImportantForNow, layerObj) in self.allMapLayers:
			if layerObj.type() == QgsMapLayer.RasterLayer:
				self.dlg.comboBox.addItem(layerObj.name())
				
		if self.dlg.comboBox.count() == 0:
			self.dlg.generateBtn.clicked.disconnect(self.sldMake)
			self.dlg.generateBtn.clicked.connect(self.noRasterLayer)

		self.dlg.exec_()#By using exec_() function the plugin window will be top most and QGIS window deactivated.