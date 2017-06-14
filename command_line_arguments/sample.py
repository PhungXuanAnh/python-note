#!/usr/bin/python

import sys, json

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:'
print (json.dumps(sys.argv, indent=4, sort_keys=True))

print ("sys.argv[1] = {}".format(sys.argv[1]))