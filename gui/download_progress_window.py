# -*- coding: utf-8 -*-
"""
import sys, os, time
import urllib2
import json
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import QThread, pyqtSignal, QObject
from PyQt4.Qt import *
"""
# from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
# from qgis.gui import QgsMessageBar
# from PyQt5 import uic

import os
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton

from module.module_download_image import DownloadWorker


class DownloadProgressWindow(QtWidgets.QWidget):

    # MAX_WINDOW_WIDTH = 600s
    MAX_NUM_DOWNLOADS = 20
    MAX_WINDOW_HEIGHT_PER_PROGRESS_BAR = 50
    POSITION_WINDOW_FROM_RIGHT = 10
    POSITION_WINDOW_FROM_BOTTOM = 50

    def __init__(self, iface=None, parent=None):
        # from PyQt5.QtCore import Qt, QDate
        # QtWidget.__init__(self)
        super().__init__(parent)
        self.iface = iface
        # self.setGeometry(300, 300, 280, 280)
        self.setWindowTitle('Download Progress')
        self.vLayout = QVBoxLayout(self)

        self.activeId = -1

    def closeEvent(self, closeEvent):
        for eachTread in self.dwThreads:
            eachTread.stop()
            eachTread.quit()

        self.clearLayout(self.vLayout)
        self.activeId = -1

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def setWindowPosition(self):
        # This part need to be modified...
        maxHeight = int(
            DownloadProgressWindow.MAX_WINDOW_HEIGHT_PER_PROGRESS_BAR * len(self.hLayouts))
        # self.setMaximumWidth(DownloadProgressWindow.MAX_WINDOW_WIDTH)
        self.setMaximumHeight(maxHeight)
        screenShape = QtWidgets.QDesktopWidget().screenGeometry()
        width, height = screenShape.width(), screenShape.height()
        winW, winH = (self.frameGeometry().width(),
                      self.frameGeometry().height())
        left = width - (
                winW + DownloadProgressWindow.POSITION_WINDOW_FROM_RIGHT)
        top = height - (
                winH + DownloadProgressWindow.POSITION_WINDOW_FROM_BOTTOM)
        # print('ScreenW: ' + str(width) + ' ScreenH:' + str(height))
        # print('WinWidth: ' + str(winW) +
        #     ' WinHeight: ' + str(winH) +
        #     ' MaxHeight: ' + str(maxHeight))
        # print('Left: ' + str(left) + ' Top: ' + str(top))
        # print('')
        self.move(left, top)
        self.activateWindow()

    def startDownload(self, url=None, fileAbsPath=None, addLayer=True):

        self.activeId += 1

        if self.activeId > DownloadProgressWindow.MAX_NUM_DOWNLOADS - 1:
            qMsgBox = QMessageBox()
            qMsgBox.setWindowTitle('Message')
            msg = "The maximum numbers of images for downloading " \
                  "is presently set to {0}.\nIf you need to " \
                  "download more, please finish the current " \
                  "uploading tasks first, and try download again" \
                  ".".format(DownloadProgressWindow.MAX_NUM_DOWNLOADS)
            qMsgBox.setText(msg)
            qMsgBox.exec_()
        else:
            # Initialize the lists
            if self.activeId == 0:
                self.hLayouts = []
                self.qLabels = []
                self.progressBars = []
                self.cancelButtons = []
                self.dwThreads = []

            # Create horizontal layouts and add to the vertical layout
            self.hLayouts.append(QHBoxLayout())
            self.vLayout.addLayout(self.hLayouts[self.activeId])

            # Create labes, progressbars, and cancel buttons,
            # and add to hLayouts
            self.qLabels.append(QLabel())

            self.progressBars.append(QProgressBar())
            self.cancelButtons.append(QPushButton('Cancel'))
            self.hLayouts[self.activeId].addWidget(
                self.qLabels[self.activeId], Qt.AlignLeft)
            self.hLayouts[self.activeId].addWidget(
                self.progressBars[self.activeId], Qt.AlignRight)
            self.hLayouts[self.activeId].addWidget(
                self.cancelButtons[self.activeId], Qt.AlignRight)

            self.progressBars[self.activeId].setFixedWidth(120)
            self.cancelButtons[self.activeId].setFixedWidth(65)

            # Set the file names to labels
            fileName = os.path.basename(fileAbsPath)
            self.qLabels[self.activeId].setText(fileName)

            # add event listener and handlers to cancel buttons
            # threadIndex = self.activeId
            # self.cancelButtons[self.activeId].clicked.connect(
            #  lambda: self.cancelDownload(threadIndex))
            self.cancelButtons[self.activeId].clicked.connect(
                self.cancelDownload)

            # self.dwThreads.append(DownloadWorker(
            #       url, fileAbsPath, addLayer, threadIndex))
            self.dwThreads.append(DownloadWorker(url,
                                                 fileAbsPath,
                                                 addLayer,
                                                 self.activeId))
            self.dwThreads[self.activeId].started.connect(
                self.downloadStarted)
            self.dwThreads[self.activeId].valueChanged.connect(
                self.updateProgressBar)
            self.dwThreads[self.activeId].finished.connect(
                self.downloadFinished)
            self.dwThreads[self.activeId].error.connect(
                self.displayError)
            self.dwThreads[self.activeId].start()
            # self.dwThread.run()
            # self.dwThread.wait()
            # self.dwThread.terminate()

            self.show()
            self.setWindowPosition()

    # def cancelDownload(self, btnIndex):
    def cancelDownload(self):
        for index in range(0, len(self.cancelButtons)):
            if self.cancelButtons[index] == self.sender():
                print('Cancel: {}'.format(str(index)))
                self.dwThreads[index].stop()

    def downloadStarted(self, hasStarted, index):
        print('Start Index:{}'.format(str(index)))
        # pass

    def updateProgressBar(self, valueChanged, index):
        # print(str(valueChanged))
        self.progressBars[index].setValue(valueChanged)

    def downloadFinished(self, result, index):
        # self.thread.quit()
        self.dwThreads[index].quit()
        print('Result: ' + result)
        try:  # make sure if the labels still exist
            if result == 'success':
                self.qLabels[index].setText("Successfully downloaded.")
                # add the downloaded image as a raster layer
                if self.dwThreads[index].addLayer:
                    layerAbsPath = self.dwThreads[index].fileAbsPath
                    layerName = str(os.path.basename(layerAbsPath))
                    self.iface.addRasterLayer(layerAbsPath, layerName)
            elif result == 'cancelled':
                self.qLabels[index].setText("Download cancelled.")
            else:
                self.qLabels[index].setText("Unexpected incident occurred.")
        except:
            pass

    def displayError(self, errMsg, index):
        print(str(errMsg))
        self.qLabels[index].setText("Error: " + str(errMsg))
