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
#from module.module_access_oam_catalog import OAMCatalogAccess
#from module.module_geocoding import nominatim_search


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/img_search_dialog.ui'))


class ImgSearchDialog(QtWidgets.QDialog, FORM_CLASS):
#class ImgSearchDialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, iface, parent=None):
    #def __init__(self, iface, settings, parent=None):
        """Constructor."""
        super(ImgSearchDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.iface = iface
        self.setupUi(self)
