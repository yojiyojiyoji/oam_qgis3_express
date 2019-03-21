# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QProgressBar, QMessageBox

from module.module_download_image import ImgDownloadWorker


class DownloadProgressWindow(QtWidgets.QWidget):

    # MAX_WINDOW_WIDTH = 600
    MAX_NUM_DOWNLOADS = 10
    MAX_WINDOW_HEIGHT_PER_PROGRESS_BAR = 50
    POSITION_WINDOW_FROM_RIGHT = 20
    POSITION_WINDOW_FROM_BOTTOM = 75

    def __init__(self, iface=None, parent=None):
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

    def initWindowPosition(self):
        screenShape = QtWidgets.QDesktopWidget().screenGeometry()
        screenWidth = screenShape.width()
        screenHeight = screenShape.height()

        winWidth = self.frameGeometry().width()
        winHeight = self.frameGeometry().height()

        posLeft = screenWidth - (winWidth + self.POSITION_WINDOW_FROM_RIGHT)
        posTop = screenHeight - (winHeight + self.POSITION_WINDOW_FROM_BOTTOM)
        self.move(posLeft, posTop)

        # print('Pos_X: {}'.format(posLeft))
        # print('Pos_Y: {}'.format(posTop))
        # print('Win Width: {}'.format(self.frameGeometry().width()))
        # print('Win Height: {}'.format(self.frameGeometry().height()))

    def adjustWindowPosition(self):
        screenShape = QtWidgets.QDesktopWidget().screenGeometry()
        screenWidth = screenShape.width()
        screenHeight = screenShape.height()

        winWidth = self.frameGeometry().width()
        winHeight = self.frameGeometry().height()

        winRight = self.pos().x() + winWidth
        winBottom = self.pos().y() + winHeight

        posLeft = self.pos().x()
        posTop = self.pos().y()

        if winRight + self.POSITION_WINDOW_FROM_RIGHT >= screenWidth:
            posLeft = screenWidth - (
                winWidth + self.POSITION_WINDOW_FROM_RIGHT)
            self.move(posLeft, self.pos().y())

        if winBottom + self.POSITION_WINDOW_FROM_BOTTOM >= screenHeight:
            posTop = screenHeight - (
                winHeight + self.POSITION_WINDOW_FROM_BOTTOM)
            self.move(self.pos().x(), posTop)

        # print('ScreenW: ' + str(screenWidth) +
        #       ' ScreenH:' + str(screenHeight))
        # print('WinWidth: ' + str(winWidth) +
        #       ' WinHeight: ' + str(winHeight))
        # print('Left: ' + str(posLeft) + ' Top: ' + str(posTop))
        # print('')

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

            self.qLabels[self.activeId].setFixedWidth(220)
            self.progressBars[self.activeId].setFixedWidth(120)
            self.cancelButtons[self.activeId].setFixedWidth(65)

            # Set the file names to labels
            fileName = os.path.basename(fileAbsPath)
            self.qLabels[self.activeId].setText(fileName)

            # add event listener and handlers to cancel buttons
            self.cancelButtons[self.activeId].clicked.connect(
                self.cancelDownload)

            self.dwThreads.append(ImgDownloadWorker(url,
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


            if self.activeId == 0:
                self.show()
                self.initWindowPosition()
            else:
                self.activateWindow()
                self.adjustWindowPosition()

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
                    insertedLayer = self.iface.addRasterLayer(
                        layerAbsPath, layerName)
                    # print(str(insertedLayer.id()))
                    # if insertedLayer:
                    #     self.iface.zoomToActiveLayer()
            elif result == 'cancelled':
                self.qLabels[index].setText("Download cancelled.")
            else:
                self.qLabels[index].setText("Unexpected incident occurred.")
        except:
            pass

    def displayError(self, errMsg, index):
        print(str(errMsg))
        self.qLabels[index].setText("Error: " + str(errMsg))
