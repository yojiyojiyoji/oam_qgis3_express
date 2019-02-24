# -*- coding: utf-8 -*-
import os, sys
#import json

from PyQt5 import uic
from PyQt5 import QtWidgets

#from PyQt4 import QtGui, uic
#from PyQt4 import QtCore
#from PyQt4.Qt import *
#from qgis.gui import QgsMessageBar

#from img_browser import ImgBrowser
from module.module_access_oam_catalog import OAMCatalogAccess
#from module.module_geocoding import nominatim_search


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/img_search_dialog.ui'))


class ImgSearchDialog(QtWidgets.QDialog, FORM_CLASS):
#class ImgSearchDialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, iface, settings, parent=None):
        """Constructor."""
        #super(ImgSearchDialog, self).__init__(parent)
        super().__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.iface = iface
        self.setupUi(self)

        self.settings = settings

        # Add event listeners and handlers
        self.pushButtonSearch.clicked.connect(self.startSearch)

        # Set URL of catalog
        self.settings.beginGroup("Storage")

        if self.settings.value('CATALOG_URL') is None or \
            str(self.settings.value('CATALOG_URL')) == '':
            # self.catalogUrl = "https://oam-catalog.herokuapp.com"
            self.catalogUrl = "http://api.openaerialmap.org"
        else:
            self.catalogUrl = str(self.settings.value('CATALOG_URL'))

        self.settings.endGroup()

    def startSearch(self):
        test = OAMCatalogAccess("https://api.openaerialmap.org", "meta", {})
        print("Results: " + str(test.getMetadataInList()))
