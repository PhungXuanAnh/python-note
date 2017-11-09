#!/usr/bin/env python
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

from cambridge_api import API
import json
import sys

api = API(baseUrl=sys.argv[1]+'/api/v1/', accessKey=sys.argv[2])

print "*** Dictionaries"
dictionaries = json.loads(api.getDictionaries())
print dictionaries

dict = dictionaries[0]
print dict
dictCode = dict["dictionaryCode"]

print "*** Search"
print "*** Result list"
results = json.loads(api.search(dictCode, "ca", 1, 1))
print results
print "*** Spell checking"
spellResults = json.loads(api.didYouMean(dictCode, "dorg", 3))
print spellResults
print "*** Best matching"
bestMatch = json.loads(api.searchFirst("british", "ca", "html"))
print(bestMatch)

print "*** Nearby Entries"
nearbyEntries = json.loads(api.getNearbyEntries(dictCode, bestMatch["entryId"], 3))
print nearbyEntries
