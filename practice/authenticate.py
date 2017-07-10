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

# Access a protected page
try:
    response = urllib2.urlopen(request)
except IOError, e:
    pass
else:
    print 'No authentication is required'
    sys.exit(0)

# Get authenticate scheme & realm
authline = e.headers['www-authenticate']
auth = re.compile(
    r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
    re.IGNORECASE)
match_auth = auth.match(authline)

print authline

scheme = match_auth.group(1)
realm = match_auth.group(2)

print scheme
print realm

# Add user authentication
base64string = base64.encodestring(
                '%s:%s' % (username, password))[:-1]
authheader =  "Basic %s" % base64string
request.add_header("Authorization", authheader)

# Re-access the page
try:
    response = urllib2.urlopen(request)
except IOError, e:
    print e.reason

read_page = response.read()
print read_page