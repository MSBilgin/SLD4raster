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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4.QtXml import QDomDocument
from PyQt4.Qsci import QsciScintilla, QsciLexerXML

import resources_rc
from dialogs import sld4rasterDialog, gsUploadDialog

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import codecs
import urllib2
import os


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
		#Saving sld or qml documents to files.
		try:
			#Firstly checking xml syntax.
			minidom.parseString(document.encode("utf-8")) #UTF encoding for non-ASCII chars.
			if type=='SLD':
				saveDlg = QFileDialog.getSaveFileName(self.dlg, 'Save SLD File...','.', 'SLD file (*.sld);; XML file (*.xml);; All files (*.*)')
				saveMessage = 'The SLD file has been succesfully saved.'
			else:
				saveDlg = QFileDialog.getSaveFileName(self.dlg, 'Save QML File...','.', 'QGIS Layer Style File (*.qml)')
				saveMessage = 'The QML file has been succesfully saved.'
				
			if saveDlg:
				try:
					with open(saveDlg, 'w') as File:
						File.write(document.encode('utf-8'))#UTF encoding for non-ASCII chars.
					QMessageBox.information(None, "Information", saveMessage)
				except Exception as saveError:
					QMessageBox.critical(None, "Information", ("An error has occured: " + str(saveError)))
					
		except Exception as error:
			QMessageBox.critical(None, "Invalid XML", str(error))			
		
	def browseFile(self):
		browseDlg = QFileDialog.getOpenFileName(self.dlg, "Choose SLD File...",".", "SLD file (*.sld);; XML file (*.xml);; All files (*.*)")
		if browseDlg:
			self.dlg.lineEdit.setText(browseDlg)
			try:
				with codecs.open(browseDlg, encoding='utf-8', mode='r') as readFile:
					self.dlg.sldText2.setText(readFile.read())
			except Exception as readError:	
				QMessageBox.critical(None, "Information", ("An error has occured: " + str(readError)))
			
	def validation(self, inputXML):			
		try:
			minidom.parseString(inputXML.encode("utf-8")) #UTF encoding for non-ASCII chars.
			QMessageBox.information(None, "Information", "The XML document is well-formed.")
		except Exception as SLDerror:
			QMessageBox.critical(None, "Invalid XML", str(SLDerror))		
			
	def sldTransform(self):		
		try:
			sldDocument = minidom.parseString(self.dlg.sldText2.text().encode('utf-8'))
			
			#Namespaces (sld, se, none) are most important part. Firstly they must be handled.
			if len(sldDocument.getElementsByTagName('sld:RasterSymbolizer')) > 0:
				nameSpace = 'sld:'
				
			elif len(sldDocument.getElementsByTagName('se:RasterSymbolizer')) > 0:
				nameSpace = 'se:'
				
			else:
				nameSpace = '' #no namespace.			
			
			#main QML structure.
			qmlRoot = Element('qgis')
			pipe = SubElement(qmlRoot, 'pipe')
		
			rasterRenderer = SubElement(pipe, 'rasterrenderer')
			rasterTransparency = SubElement(rasterRenderer,'rasterTransparency')
		
			#checking document for containing ColorMap tag. If does, it is a single-band raster.
			sldRasterType = sldDocument.getElementsByTagName(nameSpace + 'ColorMap') 
			
			if len(sldRasterType) == 0 :
				sldRedBand = sldDocument.getElementsByTagName(nameSpace + 'RedChannel')[0].getElementsByTagName(nameSpace + 'SourceChannelName')[0].firstChild.nodeValue
				sldGreenBand = sldDocument.getElementsByTagName(nameSpace + 'GreenChannel')[0].getElementsByTagName(nameSpace + 'SourceChannelName')[0].firstChild.nodeValue
				sldBlueBand = sldDocument.getElementsByTagName(nameSpace + 'BlueChannel')[0].getElementsByTagName(nameSpace + 'SourceChannelName')[0].firstChild.nodeValue
						
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
					sldColorMapType = sldDocument.getElementsByTagName(nameSpace + 'ColorMap')[0].attributes.has_key('type') #sometimes "ColorMap" tag does not contain "type" attribute. This means it is a ramp color.
					sldColorMapType2 = sldDocument.getElementsByTagName(nameSpace + 'ColorMap')[0].attributes['type'].value #or getting raster map colortype by "type" atribute.
				except:
					pass
				
				if sldColorMapType and sldColorMapType2 == 'intervals':
					colorRampShader.attrib['colorRampType'] = 'DISCRETE'
				else:
					colorRampShader.attrib['colorRampType'] = 'INTERPOLATED'
			
				sldColorValues = list()
				sldItemList = sldDocument.getElementsByTagName(nameSpace + 'ColorMapEntry')
			
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
		
			#some SLD documents don't have 'Opacity' tag so the problem is handled by this way.
			try:
				sldOpacity = sldDocument.getElementsByTagName(nameSpace + 'Opacity')[0].firstChild.nodeValue
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
			
		except Exception as sldTransformError:
			QMessageBox.critical(None, "Invalid XML", str(sldTransformError))
			
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
		self.dlg.sldText1.setText(textSLD.toprettyxml(indent = "    "))
		
	def uiSettings(self):
		self.dlg.sldText1.setMarginLineNumbers(1, True)
		self.dlg.sldText1.setMarginsBackgroundColor(QColor("#98AFC7"))
		self.dlg.sldText1.setMarginWidth(1,30)
		self.dlg.sldText1.setUtf8(True) #Enabling non-Ascii chars
		self.dlg.sldText1.setLexer(QsciLexerXML())
		
		self.dlg.sldText2.setMarginLineNumbers(1, True)
		self.dlg.sldText2.setMarginsBackgroundColor(QColor("#98AFC7"))
		self.dlg.sldText2.setMarginWidth(1,30)
		self.dlg.sldText2.setUtf8(True) #Enabling non-Ascii chars
		self.dlg.sldText2.setLexer(QsciLexerXML())
		
		self.dlg.setFixedSize(600, 615)
						
	def rememberMe(self):
		#Remember me option operation.
		try:
			if self.upDlg.checkBox.isChecked():
				flatData = self.upDlg.urlText.text() + ';' + self.upDlg.userText.text() + ';' + self.upDlg.passText.text()
				with open(os.path.join(os.path.dirname(__file__), 'int.dat'), 'w') as file:
					file.write(flatData.encode('base64'))
			
			else:
				os.remove(os.path.join(os.path.dirname(__file__), 'int.dat'))
		except Exception as error:
			QMessageBox.critical(None, "Information", str(error))
	
	def checkLogs(self):
		#Saved login data is handled in here.
		iRememberYou = os.path.isfile(os.path.join(os.path.dirname(__file__), 'int.dat'))
		if iRememberYou:
			
			with open(os.path.join(os.path.dirname(__file__), 'int.dat'), 'r') as file:
				logInData = file.read().decode('base64')
				
			try:
				self.upDlg.urlText.setText(logInData.split(';')[0])
				self.upDlg.userText.setText(logInData.split(';')[1])
				self.upDlg.passText.setText(logInData.split(';')[2])
			except:
				pass
				
			self.upDlg.checkBox.setChecked(True)
			
		else:
			self.upDlg.urlText.setText('http://localhost:8080/geoserver/rest')
			self.upDlg.userText.setText('admin')
			self.upDlg.passText.setText('geoserver')	

	def showUploadDialog(self):
		try:
			minidom.parseString(self.dlg.sldText1.text().encode('utf-8'))
			
			self.upDlg.sldText.setText(self.dlg.comboBox.currentText())
			self.upDlg.sldText.setFocus()
			self.checkLogs()
			self.upDlg.exec_()			
		except Exception as error:
			QMessageBox.critical(None, "Invalid XML", str(error))
		
	def upload(self):
		###Everything about uploding data to GeoServer is handling in here.
		status = 1 #I use it for managing operations. If status = 0 nothing to do.
		if not self.upDlg.urlText.text() or not self.upDlg.userText.text() or not self.upDlg.passText.text() or not self.upDlg.sldText.text():
			QMessageBox.critical(None, 'Information', 'Please fill in all fields.')
			
		else:
			username = self.upDlg.userText.text()
			password = self.upDlg.passText.text()
			sldName = self.upDlg.sldText.text()			
			basicLogin = 'Basic ' + (username + ':' + password).encode('base64').rstrip() #Base64 auth for REST service.
			
			#Deleting the SLD if exists on GeoServer.			
			if self.upDlg.urlText.text() [-1] == '/':
				usableUrl = self.upDlg.urlText.text()[:len(self.upDlg.urlText.text())-1] #Maybe user add slash '/' in the end of url, so this problem is solved in this way.
			else:																		 #I didnt use urlparse lib. Because this solution is simplier than it. 
				usableUrl = self.upDlg.urlText.text()
				
			url = usableUrl + '/styles/' + sldName +'?recurse=true'
			request = urllib2.Request(url)
			request.add_header("Authorization", basicLogin)
			request.get_method = lambda: 'DELETE'
			try:
				urllib2.urlopen(request)
			except Exception as deleteError:
				pass
				
			#Generating new SLD on GeoServer.
			url = usableUrl + '/styles'
			request = urllib2.Request(url)
			request.add_header("Authorization", basicLogin)
			request.add_header("Content-type", "text/xml")
			request.add_header("Accept", "*/*")
			request.add_data('<style><name>' + sldName + '</name><filename>' + (sldName + '.sld') + '</filename></style>') #
			try:
				urllib2.urlopen(request)
			except Exception as generateError:
				QMessageBox.critical(None, 'Information', str(generateError))
				status = 0
				
			#Uploading SLD to GeoServer.
			if status == 1:
				url = usableUrl + '/styles/' + sldName
				request = urllib2.Request(url)
				request.add_header("Authorization", basicLogin)
				request.add_header("Content-type", "application/vnd.ogc.sld+xml")
				request.add_header("Accept", "*/*")
				request.add_data(self.dlg.sldText1.text())
				request.get_method = lambda: 'PUT'
				try:
					urllib2.urlopen(request)
				except Exception as generateError:
					QMessageBox.critical(None, 'Information', str(generateError))
					status = 0
					
			if status == 1:
				QMessageBox.information(None, 'Information', 'The style was succesfully uploaded.')	

	def run(self):
		self.dlg = sld4rasterDialog()
		self.upDlg = gsUploadDialog()
		
		self.uiSettings() #UI elements' initial configurations.
		
		self.dlg.generateBtn.clicked.connect(self.sldMake)
		self.dlg.translateBtn.clicked.connect(self.sldTransform)
		self.dlg.saveBtn.clicked.connect(lambda: self.saveFile(self.dlg.sldText1.text(), 'SLD'))
		self.dlg.browseBtn.clicked.connect(self.browseFile)
		self.dlg.validateBtn.clicked.connect(lambda: self.validation(self.dlg.sldText1.text()))
		self.dlg.validateBtn_2.clicked.connect(lambda: self.validation(self.dlg.sldText2.text()))
		self.allMapLayers = QgsMapLayerRegistry.instance().mapLayers().items()

		for (notImportantForNow, layerObj) in self.allMapLayers:
			if layerObj.type() == QgsMapLayer.RasterLayer:
				self.dlg.comboBox.addItem(layerObj.name())
				
		if self.dlg.comboBox.count() == 0:
			self.dlg.generateBtn.clicked.disconnect(self.sldMake)
			self.dlg.generateBtn.clicked.connect(self.noRasterLayer)
						
		self.dlg.UpDlgBtn.clicked.connect(self.showUploadDialog)
		self.upDlg.uploadBtn.clicked.connect(self.upload)
		self.upDlg.checkBox.stateChanged.connect(self.rememberMe)

		self.dlg.exec_()#By using exec_() function the plugin window will be top most and QGIS window deactivated.