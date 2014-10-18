SLD4raster v0.9
==========


(C) 2014 by Mehmet Selim BILGIN

mselimbilgin [at] yahoo.com

http://cbsuygulama.wordpress.com



###Description
QGIS 2 plugin to generate SLD (Styled Layer Descriptor) for raster layers. Also it can transform SLD documents to QGIS Layer Style File (*.qgs). It supports multiband, singleband pseudocolor, gradient (white to black, black to white) styles also color interpolation type and opacity levels. Integrated with GeoServer Rest API. Provides direct upload of the styles. By using it you can share your raster map styles in QGIS with other GIS softwares that support OGC SLD standarts. For example Udig, GeoServer, MapServer…



###Features
   
   - Multiband color styles. You can use different band orders (4,3,2 or 1,2,3 etc.)

   - Singleband pseudocolor style. Color interpolation could be preferred.

   - Gradient color (white to black, black to white) styles. Also you can adjust min-max values.

   - Supports layer opacity.
  
   - SLD to QGIS Style File (*.qgs) transformation.
   
   - Integrated with GeoServer Rest API.
   
   

<p align="center">
  <img src="https://lh4.googleusercontent.com/-X9GYJoQrRqA/VELMPpwAjaI/AAAAAAAAAsQ/I39zTCnwSeM/w524-h553-no/3.png"/>
  <img src="https://lh4.googleusercontent.com/-Ila6E_AZIV8/VELMPp_e_fI/AAAAAAAAAsU/mGNpAQfhy14/w522-h553-no/2.png"/>
</p>


###Installation

1. Donwload the project and unzip it. 
2. Change the plugin folder name to SLD4raster. 
3. Copy this folder to .qgis2\python\plugins\  
