# -*- coding: utf-8 -*-
import os, sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from qgis.gui import QgsMessageBar

from module.module_access_oam_catalog import OAMCatalogAccess
from module.module_geocoding import nominatim_search
from .img_browser import ImgBrowser


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/img_search_dialog.ui'))


class ImgSearchDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, iface, settings, parent=None):
        """Constructor."""
        super().__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.iface = iface
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint)

        self.settings = settings

        # Initialize GUI
        self.initGui()

        # Initialize search queries
        self.initQueries()

        # Add Message Bar
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed)
        self.verticalLayoutListWidget.layout().addWidget(self.bar)

        # Add event listeners and handlers
        self.pushButtonSearch.clicked.connect(self.startSearch)
        self.listWidget.itemClicked.connect(self.browseThumbnailAndMeta)
        self.pbSetDefault.clicked.connect(self.setDeafult)
        self.pbLoadDefault.clicked.connect(self.loadDeafult)

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

        self.imgBrowser = None

    def initGui(self):
        item = QListWidgetItem()
        item.setText("Please set the conditions and press 'Search' button.")
        item.setData(Qt.UserRole, "Sample Data")
        self.listWidget.addItem(item)

    def initQueries(self):
        self.settings.beginGroup("ImageSearch")
        if self.settings.value('CHECKBOX_LOCATION') is None:
            print('create new queries settings')
            self.createQSettingsQueries()
        self.settings.endGroup()
        self.loadQSettingsQueries()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.startSearch()

    def setDeafult(self):
        print('Set Default Queries')
        self.saveQSettingsQueries()

    def loadDeafult(self):
        print('Load Default Queries')
        self.loadQSettingsQueries()

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
                # print(strBboxForOAM)
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

            # print(self.comboBoxOrderBy.currentText())


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

    def createQSettingsQueries(self):
        self.settings.setValue('CHECKBOX_LOCATION', True)
        self.settings.setValue('CHECKBOX_ACQUISITION_FROM', True)
        self.settings.setValue('CHECKBOX_ACQUISITION_TO', True)
        self.settings.setValue('CHECKBOX_GSD_FROM', True)
        self.settings.setValue('CHECKBOX_GSD_TO', True)

        self.settings.setValue('LOCATION', '')
        self.settings.setValue('ACQUISITION_FROM',
            QDate.currentDate().addMonths(-12).toString(Qt.ISODate))
        self.settings.setValue('ACQUISITION_TO',
            QDate.currentDate().toString(Qt.ISODate))
        self.settings.setValue('GSD_FROM', '')
        self.settings.setValue('GSD_TO', '')
        self.settings.setValue('LIMIT', 20)
        self.settings.setValue('ORDER_BY', 0)
        self.settings.setValue('SORT', 'desc')

    def loadQSettingsQueries(self):
        self.settings.beginGroup("ImageSearch")

        if str(self.settings.value('CHECKBOX_LOCATION')).lower() == 'true':
            self.checkBoxLocation.setCheckState(2)
        else:
            self.checkBoxLocation.setCheckState(0)
        if str(self.settings.value('CHECKBOX_ACQUISITION_FROM')).lower() == 'true':
            self.checkBoxAcquisitionFrom.setCheckState(2)
        else:
            self.checkBoxAcquisitionFrom.setCheckState(0)
        if str(self.settings.value('CHECKBOX_ACQUISITION_TO')).lower() == 'true':
            self.checkBoxAcquisitionTo.setCheckState(2)
        else:
            self.checkBoxAcquisitionTo.setCheckState(0)
        if str(self.settings.value('CHECKBOX_GSD_FROM')).lower() == 'true':
            self.checkBoxResolutionFrom.setCheckState(2)
        else:
            self.checkBoxResolutionFrom.setCheckState(0)
        if str(self.settings.value('CHECKBOX_GSD_TO')).lower() == 'true':
            self.checkBoxResolutionTo.setCheckState(2)
        else:
            self.checkBoxResolutionTo.setCheckState(0)

        self.lineEditLocation.setText(
            self.settings.value('LOCATION'))
        self.dateEditAcquisitionFrom.setDate(QDate.fromString(
            self.settings.value('ACQUISITION_FROM'), Qt.ISODate))
        self.dateEditAcquisitionTo.setDate(QDate.fromString(
            self.settings.value('ACQUISITION_TO'), Qt.ISODate))
        self.lineEditResolutionFrom.setText(
            str(self.settings.value('GSD_FROM')))
        self.lineEditResolutionTo.setText(
            str(self.settings.value('GSD_TO')))
        self.lineEditNumImages.setText(
            str(self.settings.value('LIMIT')))
        self.comboBoxOrderBy.setCurrentIndex(
            int(self.settings.value('ORDER_BY')))
        if self.settings.value('SORT') == 'desc':
            self.radioButtonDesc.setChecked(True)
        else:
            self.radioButtonAsc.setChecked(True)

        self.settings.endGroup()

    def saveQSettingsQueries(self):
        self.settings.beginGroup("ImageSearch")

        self.settings.setValue('CHECKBOX_LOCATION',
            self.checkBoxLocation.isChecked())
        self.settings.setValue('CHECKBOX_ACQUISITION_FROM',
            self.checkBoxAcquisitionFrom.isChecked())
        self.settings.setValue('CHECKBOX_ACQUISITION_TO',
            self.checkBoxAcquisitionTo.isChecked())
        self.settings.setValue('CHECKBOX_GSD_FROM',
            self.checkBoxResolutionFrom.isChecked())
        self.settings.setValue('CHECKBOX_GSD_TO',
            self.checkBoxResolutionTo.isChecked())

        self.settings.setValue('LOCATION',
            self.lineEditLocation.text())
        self.settings.setValue('ACQUISITION_FROM',
            self.dateEditAcquisitionFrom.date().toString(Qt.ISODate))
        self.settings.setValue('ACQUISITION_TO',
            self.dateEditAcquisitionTo.date().toString(Qt.ISODate))
        if (self.lineEditResolutionFrom.text() != ''
            and self.lineEditResolutionFrom.text() is not None):
            self.settings.setValue('GSD_FROM',
                float(self.lineEditResolutionFrom.text()))
        if (self.lineEditResolutionTo.text() != ''
            and self.lineEditResolutionTo.text() is not None):
            self.settings.setValue('GSD_TO',
                float(self.lineEditResolutionTo.text()))
        if (self.lineEditNumImages.text() != ''
            and self.lineEditNumImages.text() is not None):
            self.settings.setValue('LIMIT',
                int(self.lineEditNumImages.text()))
        self.settings.setValue('ORDER_BY',
            self.comboBoxOrderBy.currentIndex())
        if self.radioButtonDesc.isChecked():
            self.settings.setValue('SORT', 'desc')
        else:
            self.settings.setValue('SORT', 'asc')

        self.settings.endGroup()

    def browseThumbnailAndMeta(self, item):

        singleMetaInDict = item.data(Qt.UserRole)
        # print(str(singleMetaInDict))

        if self.imgBrowser is None:
            self.imgBrowser = ImgBrowser(self.iface)

            pos = self.pos()
            # print(pos.x())
            # print(pos.y())
            pos.setX(pos.x() + 400)
            pos.setY(pos.y() + 20)
            self.imgBrowser.move(pos)

        if not self.imgBrowser.isVisible():
            self.imgBrowser.show()

        self.imgBrowser.setSingleMetaInDict(singleMetaInDict)
        self.imgBrowser.displayMetadata()
        self.imgBrowser.displayThumbnail()

        self.imgBrowser.activateWindow()
