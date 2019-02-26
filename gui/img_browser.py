# -*- coding: utf-8 -*-
import os
from dateutil import parser

from PyQt5 import uic
from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/img_browser.ui'))


class ImgBrowser(QtWidgets.QDialog, FORM_CLASS):

    POSITION_WINDOW_FROM_RIGHT = 50
    POSITION_WINDOW_FROM_TOP = 100

    def __init__(self, iface, parent=None):
        """Constructor."""
        #super(OAMQGIS3Dialog, self).__init__(parent)
        super().__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.iface = iface
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint)

        screenShape = QtWidgets.QDesktopWidget().screenGeometry()
        width, height = screenShape.width(), screenShape.height()
        winW, winH = (self.frameGeometry().width(),
                      self.frameGeometry().height())
        left = width - (winW + ImgBrowser.POSITION_WINDOW_FROM_RIGHT)
        top = ImgBrowser.POSITION_WINDOW_FROM_TOP
        self.move(left, top)

        self.singleMetaInDict = None

    def setSingleMetaInDict(self, singleMetaInDict):
        self.singleMetaInDict = singleMetaInDict

    def displayMetadata(self):
        # self.setDefaultGraphicsView()
        aquisitionStart = parser.parse(str(self.singleMetaInDict[u'acquisition_start']))
        strAcquisitionStart = aquisitionStart.strftime('%Y-%m-%d %H:%M (%Z)')
        # print(aquisitionStart.strftime('%Y-%m-%d %I:%M %p (%Z)'))
        aquisitionEnd = parser.parse(str(self.singleMetaInDict[u'acquisition_end']))
        strAcquisitionEnd = aquisitionEnd.strftime('%Y-%m-%d %H:%M (%Z)')
        # print(aquisitionEnd.strftime('%Y-%m-%d %I:%M %p (%Z)'))

        gsdForDisplay = float(int(self.singleMetaInDict[u'gsd'] * 100)) / 100
        fileSizeInMb = float(self.singleMetaInDict[u'file_size']) / (1000 * 1000)
        fileSizeInMb = float(int(fileSizeInMb * 100)) / 100
        # fileSizeInMb = self.singleMetaInDic[u'file_size'] / (1024 * 1024)

        strTitle = 'TITLE:\n' + self.singleMetaInDict[u'title'] + '\n'
        self.lbTitle.setWordWrap(True)
        self.lbTitle.setText(strTitle)

        strPlatform = self.singleMetaInDict[u'platform']
        strGsdForDisplay = str(gsdForDisplay) + ' m'
        strProvider = self.singleMetaInDict[u'provider']
        strFileSizeInMb = str(fileSizeInMb) + ' MB'

        self.lbText0.setText(strPlatform)
        self.lbText1.setText(strAcquisitionStart)
        self.lbText2.setText(strAcquisitionEnd)
        self.lbText3.setText(strGsdForDisplay)
        self.lbText4.setText(strProvider)
        self.lbText5.setText(strFileSizeInMb)

        # print(self.formLayoutMetadata.formAlignment())
        self.formLayoutMetadata.setLabelAlignment(Qt.AlignLeft)

        return True
