# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal

import urllib3
import chardet
import idna
import requests

from urllib.request import urlopen

class DownloadWorker(QThread):

    started = pyqtSignal(bool, int)
    valueChanged = pyqtSignal(int, int)
    finished = pyqtSignal(str, int)
    error = pyqtSignal(Exception, int)

    def __init__(self, url, fileAbsPath, addLayer=None, index=None):
        QThread.__init__(self)
        self.url = url
        self.fileAbsPath = fileAbsPath
        self.addLayer = addLayer
        self.index = index
        self.isRunning = True
        # self.delay = 0.02

    def run(self):
        try:

            self.started.emit(True, self.index)
            u = urlopen(self.url, timeout=20)
            f = open(self.fileAbsPath, 'wb')
            meta = u.info()
            fileSize = int(meta['Content-Length'])
            # print("Downloading: {0} Bytes: {1}".format(
            #                    str(self.url), str(fileSize)))
            fileSizeDownloaded = 0
            blockSize = 8192  # make sure if this block size is apropriate
            while True:
                buffer = u.read(blockSize)
                if not buffer or self.isRunning is False:
                    break
                fileSizeDownloaded += len(buffer)
                f.write(buffer)
                p = float(fileSizeDownloaded) / fileSize
                self.valueChanged.emit(int(p * 100), self.index)
            f.close()

            """
            self.started.emit(True, self.index)
            h = requests.head(self.url)
            fileSize = int(h.headers['Content-Length'])
            fileSizeDownloaded = 0
            blockSize = 8192
            fileSizeDownloaded = 0
            # print("Downloading: {0} Bytes: {1}".format(
            #                 str(self.url), str(fileSize)))

            r = requests.get(self.url, stream=True, timeout=20)
            with open(self.fileAbsPath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=blockSize):
                    if not chunk or self.isRunning is False:
                        break
                    f.write(chunk)
                    # f.flush()
                    fileSizeDownloaded += blockSize
                    p = float(fileSizeDownloaded) / fileSize
                    self.valueChanged.emit(int(p * 100), self.index)
                    # print('{}/{} : {}% index:{}'.format(
                    #     fileSizeDownloaded, fileSize, int(p * 100), self.index))
                f.close()
            """

            if self.isRunning is True:
                self.finished.emit('success', self.index)
            else:
                self.finished.emit('cancelled', self.index)

        except Exception as e:
            print(e)
            self.error.emit(e, self.index)

    def stop(self):
        self.isRunning = False
