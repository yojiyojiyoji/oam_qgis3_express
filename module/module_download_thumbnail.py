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
        # print(urlThumbnail)
        # Concatenate fileName with id to avoid duplicate filename
        imgFileName = urlThumbnail.split('/')[-1]
        imgFileName = prefix + imgFileName
        imgAbspath = os.path.join(imgDirAbspath, imgFileName)
        # print(imgAbspath)
        if not os.path.exists(imgAbspath):
            try:
                """
                response = urllib2.urlopen(urlThumbnail)
                chunkSize = 1024 * 16
                f = open(imgAbspath, 'wb')
                while True:
                    chunk = response.read(chunkSize)
                    if not chunk:
                        break
                    f.write(chunk)
                f.close()
                self.statusChanged.emit(1)
                """

                """It is better to chunk files to download"""
                r = requests.get(urlThumbnail)
                f = open(imgAbspath, 'wb')
                f.write(r.content)
                f.close()
                self.statusChanged.emit(1)

            except Exception as e:
                imgAbspath = 'failed'
                self.error.emit(e)
        # print(imgAbspath)
        return imgAbspath
