# -*- coding: utf-8 -*-
import sys
import json

import urllib3
import chardet
import idna
import requests


class OAMCatalogAccess:

    def __init__(self, hostUrl, action=None, dictQueries=None, parent=None):
        # probably need to make a textbox for editing hostUrl later
        self.hostUrl = hostUrl
        self.action = action
        self.dictQueries = dictQueries
        self.endPoint = None

    def setAction(self, action):
        self.action = action

    def setDictQueries(self, dictQueries):
        self.dictQueries = dictQueries

    def getMetadataInList(self):
        jMetadata = self.downloadMetadata()
        metadadaInDic = json.loads(jMetadata)
        metadataInList = metadadaInDic[u'results']
        return metadataInList

    def downloadMetadata(self):
        print("Query: " + str(self.dictQueries))

        self.endPoint = self.hostUrl

        if self.action is not None and self.action != '':
            self.endPoint += '/' + self.action

            # make sure how to handle location
            # if self.dictQueries.get('location') != '':
            #     pass

            count = 0
            for key in self.dictQueries:
                print(str(key) + " " + str(self.dictQueries[key]))
                if (self.dictQueries[key] is not None and
                        self.dictQueries[key] != ''):
                    if count == 0:
                        self.endPoint += '?'
                    else:
                        self.endPoint += '&'
                    self.endPoint += str(key) + "=" + str(self.dictQueries[key])
                    count += 1
        print("Endpoint: " + str(self.endPoint))

        r = requests.get(str(self.endPoint))
        #print(repr(r))
        #print(repr(r.text))
        return r.text

    def uploadMetaData(self):
        # access to self.hostUrl and upload metadata
        # invoked form uploader wizard in the future
        print("Under construction")
