# -*- coding: utf-8 -*-
import os
from dateutil import parser

from PyQt5 import uic
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from module.module_download_thumbnail import ThumbnailDownloadWorker
from module.module_download_img_metadata import ImgMetaDownloadWorker
from gui.download_progress_window import DownloadProgressWindow


# This loads your .ui file so that PyQt can populate your plugin with
# the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/img_browser.ui'))


class ImgBrowser(QDialog, FORM_CLASS):

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

        self.lbThumbnail.setAlignment(Qt.AlignCenter)

        defaultImgAbsPath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'temp', 'oam-logo.png')
        lbWidth = self.lbThumbnail.width()
        lbHeight = self.lbThumbnail.height()
        imgThumbnail = QPixmap(defaultImgAbsPath)
        self.lbThumbnail.setPixmap(
            imgThumbnail.scaled(lbWidth, lbHeight,Qt.KeepAspectRatio))

        self.pushButtonDownload.clicked.connect(self.downloadFullImage)
        # self.connect(self.pushButtonDownload,
        #              QtCore.SIGNAL("clicked()"),
        #              self.downloadFullImage)

        self.checkBoxSaveMeta.setChecked(True)

        self.singleMetaInDict = None
        self.thumbDownWorker = ThumbnailDownloadWorker()

        self.downloadProgressWindow = None

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

    def displayThumbnail(self):
        isDownloadSuccess = False
        urlThumbnail = self.singleMetaInDict[u'properties'][u'thumbnail']
        imageId = self.singleMetaInDict[u'_id']
        prefix = str(imageId) + '_'
        imgAbspath = self.thumbDownWorker.downloadThumbnail(urlThumbnail, prefix)

        if imgAbspath != 'failed':
            isDownloadSuccess = True
            lbWidth = self.lbThumbnail.width()
            lbHeight = self.lbThumbnail.height()
            imgThumbnail = QPixmap(imgAbspath)
            self.lbThumbnail.setPixmap(
                imgThumbnail.scaled(lbWidth, lbHeight,Qt.KeepAspectRatio))
        else:
            self.setDefaultThumbnail()

        return isDownloadSuccess

    def setDefaultThumbnail(self):
        defaultImgAbsPath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'temp', 'oam-logo.png')
        lbWidth = self.lbThumbnail.width()
        lbHeight = self.lbThumbnail.height()
        imgThumbnail = QPixmap(defaultImgAbsPath)
        self.lbThumbnail.setPixmap(
            imgThumbnail.scaled(lbWidth, lbHeight,Qt.KeepAspectRatio))

    def downloadFullImage(self):
        urlFullImage = self.singleMetaInDict[u'uuid']
        imgFileName = urlFullImage.split('/')[-1]
        defaultDir = os.path.join(os.path.expanduser('~'), 'oam_images')
        imgAbsPath = os.path.join(defaultDir, imgFileName)
        if not os.path.exists(defaultDir):
            os.makedirs(defaultDir)

        # fdlg = QFileDialog()
        # fdlg.setDefaultSuffix('tif')
        # fdlg.setAcceptMode(QFileDialog.AcceptSave)
        # fdlg.selectFile(imgAbsPath)
        # fdlg.setFilter("GEOTiff")
        rSfn = QFileDialog.getSaveFileName(
            None, 'Save As', imgAbsPath, "TIF Files (*.tif)")
        imgAbsPath = rSfn[0]

        # if fdlg.exec_():
        if imgAbsPath != '':
            # Download image metadata first
            if self.checkBoxSaveMeta.isChecked():
                try:
                    urlImgMeta = self.singleMetaInDict[u'meta_uri']
                    # print(urlImgMeta)
                    # print(imgAbsPath)
                    posLastDots = imgAbsPath.rfind('.')

                    if imgAbsPath[posLastDots:] != '.tif':
                        imgMetaAbsPath = imgAbsPath + '_meta.json'
                    else:
                        imgMetaAbsPath = imgAbsPath[0:posLastDots] + '_meta.json'

                    # print(imgMetaAbsPath)
                    # imgMetaFilename = urlImgMeta.split('/')[-1]
                    # imgMetaAbsPath = os.path.join(
                    #    os.path.dirname(imgAbsPath),
                    #    imgMetaFilename)
                    r = ImgMetaDownloadWorker.downloadImgMeta(
                        urlImgMeta,
                        imgMetaAbsPath)
                    # print(str(r))
                except:
                    print('Problem occurred for downloading image metadata.')

            # Download image
            # Need excepton handling here?
            if self.downloadProgressWindow is None:
                self.downloadProgressWindow = DownloadProgressWindow(self.iface)

            if self.checkBoxAddLayer.isChecked():
                addLayer = True
            else:
                addLayer = False

            self.downloadProgressWindow.startDownload(
                urlFullImage, imgAbsPath, addLayer)
