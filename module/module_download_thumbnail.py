# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QThread, pyqtSignal, QObject

import urllib3
import chardet
import idna
import requests

class ThumbnailManager(QObject):

    statusChanged = pyqtSignal(int)
    error = pyqtSignal(Exception)

    def __init__(self, parent=None):
        QObject.__init__(self)

    def downloadThumbnail(self, urlThumbnail, prefix):
        self.statusChanged.emit(0)
        imgDirAbspath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'temp')
        imgFileName = urlThumbnail.split('/')[-1]
        imgFileName = prefix + imgFileName
        imgAbspath = os.path.join(imgDirAbspath, imgFileName)
        # print(urlThumbnail)
        # print(imgAbspath)

        if not os.path.exists(imgAbspath):
            try:
                r = requests.get(urlThumbnail)
                f = open(imgAbspath, 'wb')
                f.write(r.content)
                f.close()
                self.statusChanged.emit(1)
                """
                r = requests.get(urlThumbnail, stream=True)
                with open(imgAbspath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
                    f.close()
                self.statusChanged.emit(1)
                """
            except Exception as e:
                imgAbspath = 'failed'
                self.error.emit(e)

        return imgAbspath
