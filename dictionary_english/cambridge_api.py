#
# Copyright (c) 2012, IDM
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
#     * Neither the name of the IDM nor the names of its contributors may be used to endorse or
#       promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from urllib import (urlencode, quote)
import urllib2

class API(object):

    def _getBaseUrl(self):
        return self._baseUrl

    def _setBaseUrl (self, baseUrl):
        if baseUrl and baseUrl[-1] != '/':
            self._baseUrl = baseUrl + '/'
        else:
            self._baseUrl = baseUrl

    baseUrl = property(_getBaseUrl, _setBaseUrl)

    def __init__(self, baseUrl, accessKey, userAgent = urllib2):
        self.baseUrl = baseUrl
        self.accessKey = accessKey
        self.userAgent = userAgent

    def _buildUrl(self, *pathParts, **queryParts):
        uri = self._baseUrl
        uri += "/".join([quote(p) for p in pathParts])

        nonNullQueryParts = {}
        for paramName, paramValue in queryParts.iteritems():
            if paramValue is not None:
                nonNullQueryParts[paramName] = paramValue
        if nonNullQueryParts:
            uri +=  "?%s" % urlencode(nonNullQueryParts)
        return uri

    def _open(self, url):
        request = self._prepareGetRequest(url)
        response = self.userAgent.urlopen(request)
        body = response.read()
        return body

    def _prepareGetRequest(self, url):
        request = self.userAgent.Request(url)
        request.add_header('accessKey', self.accessKey)
        return request

    def getDictionaries(self):
        url = self._buildUrl('dictionaries')
        return self._open(url)

    def getDictionary(self, dictionaryCode):
        url = self._buildUrl('dictionaries', dictionaryCode)
        return self._open(url)

    def getEntry (self, dictionaryCode, entryId, entryFormat=None):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              format=entryFormat)
        return self._open(url)

    def getEntryPronunciations (self, dictionaryCode, entryId, lang):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              'pronunciations',
                              lang=lang)
        return self._open(url)

    def getNearbyEntries (self, dictionaryCode, entryId, entryNumber=None):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              'nearbyentries',
                              entrynumber=entryNumber)
        return self._open(url)

    def getRelatedEntries (self, dictionaryCode, entryId):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              'relatedentries')
        return self._open(url)

    def getWordOfTheDay(self, dictionaryCode=None, day=None, entryFormat=None):
        params = dict(day=day, format=entryFormat)
        url = None
        if dictionaryCode is not None:
            url = self._buildUrl('dictionaries',
                                  dictionaryCode,
                                  'wordoftheday',
                                  **params)
        else:
            url = self._buildUrl('wordoftheday',
                                 **params)
        return self._open(url)

    def getWordOfTheDayPreview(self, dictionaryCode=None, day=None):
        params = dict(day=day)
        url = None
        if dictionaryCode is not None:
            url = self._buildUrl('dictionaries',
                                  dictionaryCode,
                                  'wordoftheday',
                                  'preview',
                                  **params)
        else:
            url = self._buildUrl('wordoftheday',
                                  'preview',
                                  **params)
        return self._open(url)

    def search(self, dictionaryCode, searchWord, pageSize=None, pageIndex=None) :
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'search',
                              q=searchWord,
                              pagesize=pageSize,
                              pageindex=pageIndex)
        return self._open(url)

    def searchFirst (self, dictionaryCode, searchWord, entryFormat=None):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'search',
                              'first',
                              q=searchWord,
                              format=entryFormat)
        return self._open(url)

    def didYouMean(self, dictionaryCode, searchWord, entryNumber=None):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'search',
                              'didyoumean',
                              q=searchWord,
                              entrynumber=entryNumber)
        return self._open(url)

    def getThesaurusList(self, dictionaryCode):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'topics')
        return self._open(url)

    def getTopic (self, dictionaryCode, thesName, topicId):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'topics',
                              thesName,
                              topicId)
        return self._open(url)
