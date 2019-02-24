# -*- coding: utf-8 -*-
import os, sys
#import json

from PyQt5 import uic
from PyQt5 import QtWidgets

#from PyQt4 import QtGui, uic
#from PyQt4 import QtCore
#from PyQt4.Qt import *
#from qgis.gui import QgsMessageBar

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

#from img_browser import ImgBrowser
from module.module_access_oam_catalog import OAMCatalogAccess
from module.module_geocoding import nominatim_search


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

        self.oamCatalogAccess = OAMCatalogAccess(self.catalogUrl)
        catalogUrlLabel = self.catalog_url_label.text() + self.catalogUrl
        self.catalog_url_label.setText(catalogUrlLabel)

    def refreshListWidget(self, metadataInList):

        self.listWidget.clear()

        for singleMetaInDict in metadataInList:
            item = QListWidgetItem()
            item.setText(singleMetaInDict[u'title'])
            item.setData(Qt.UserRole, singleMetaInDict)
            self.listWidget.addItem(item)

    def startSearch(self):
        action = "meta"
        dictQueries = {}

        try:
            if self.checkBoxLocation.isChecked():
                location = self.lineEditLocation.text()
                strBboxForOAM = nominatim_search(location)
                print(strBboxForOAM)
                if strBboxForOAM != 'failed':
                    dictQueries['bbox'] = strBboxForOAM
                else:
                    qMsgBox = QMessageBox()
                    qMsgBox.setWindowTitle('Message')
                    qMsgBox.setText("The 'location' won't be used as a " +
                                    "query, because Geocoder could " +
                                    "not find the location.")
                    qMsgBox.exec_()

            if self.checkBoxAcquisitionFrom.isChecked():
                dictQueries['acquisition_from'] = \
                    self.dateEditAcquisitionFrom.date().toString(Qt.ISODate)

            if self.checkBoxAcquisitionTo.isChecked():
                dictQueries['acquisition_to'] = \
                    self.dateEditAcquisitionTo.date().toString(Qt.ISODate)

            if self.checkBoxResolutionFrom.isChecked():
                if (self.lineEditResolutionFrom.text() != '' and
                        self.lineEditResolutionFrom.text() is not None):
                    dictQueries['gsd_from'] = \
                        float(self.lineEditResolutionFrom.text())

            if self.checkBoxResolutionTo.isChecked():
                if (self.lineEditResolutionTo.text() != '' and
                        self.lineEditResolutionTo.text() is not None):
                    dictQueries['gsd_to'] = \
                        float(self.lineEditResolutionTo.text())

            if (self.lineEditNumImages.text() != '' and
                    self.lineEditNumImages.text() is not None):
                dictQueries['limit'] = int(self.lineEditNumImages.text())

            if self.comboBoxOrderBy.currentText() == 'Acquisition Date':
                dictQueries['order_by'] = "acquisition_end"
            elif self.comboBoxOrderBy.currentText() == 'GSD':
                dictQueries['order_by'] = "gsd"

            print(self.comboBoxOrderBy.currentText())


            if self.radioButtonAsc.isChecked():
                dictQueries['sort'] = "asc"
            elif self.radioButtonDesc.isChecked():
                dictQueries['sort'] = "desc"

            self.oamCatalogAccess.setAction(action)
            self.oamCatalogAccess.setDictQueries(dictQueries)
            metadataInList = self.oamCatalogAccess.getMetadataInList()

            self.refreshListWidget(metadataInList)

        except Exception as e:
            print(repr(e))
            qMsgBox = QMessageBox()
            qMsgBox.setWindowTitle('Message')
            qMsgBox.setText("Please make sure if you entered valid data" +
                            "/internet connection, and try again.")
            qMsgBox.exec_()

    def testStartSearch(self):
        test = OAMCatalogAccess("https://api.openaerialmap.org", "meta", {})
        print("Results: " + str(test.getMetadataInList()))
