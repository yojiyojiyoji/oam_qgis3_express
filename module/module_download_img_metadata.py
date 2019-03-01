# -*- coding: utf-8 -*-
import urllib3
import chardet
import idna
import requests


class ImgMetaDownloadWorker:
    def __init__(self, parent=None):
        pass

    @staticmethod
    def downloadImgMeta(urlImgMeta, imgMetaAbsPath):
        try:
            r = requests.get(urlImgMeta)
            f = open(imgMetaAbsPath, 'w')
            f.write(r.text)
            f.close()

        except Exception as e:
            print(str(e))

        return True
