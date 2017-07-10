import urllib
import urllib2
import sys
import re
import base64
from urlparse import urlparse


# Authenticate manually
"""
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
"""

# Authenticate with a basic handler
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
username = 'scraper4f'
password = 'scraper123'

top_url = 'https://bitbucket.org/'
target_url = 'https://bitbucket.org/dashboard/repositories'

# Add user setting to password manager
password_mgr.add_password(None, top_url, username, password)

# Create basic authentication handler
auth_basic_handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# Create & install opener
opener = urllib2.build_opener(auth_basic_handler)
urllib2.install_opener(opener)

# Access the page
response = urllib2.urlopen(target_url)
read_page = response.read()

print read_page
