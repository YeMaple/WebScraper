import urllib
import urllib2
import sys
import re
import base64
from urlparse import urlparse

url = 'https://bitbucket.org/dashboard/repositories'
request = urllib2.Request(url)

username = 'scraper4f'
password = 'scraper123'

try:
	response = urllib2.urlopen(request)
except IOError, e:
	if e.code != 401:
		print 'A different exception has occured'
		print e.code
	else:
		print e.headers
		#print e.headers['www-authenticate']