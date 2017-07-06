import urllib
import urllib2

response = urllib2.urlopen('http://www.google.com/')
html = response.read()
print html

request = urllib2.Request('http://www.google.com/')
response = urllib2.urlopen(request)
read_page = response.read()
print read_page

# Post method of http request
url = 'http://www.server.come/register.jsp'
values = { 'name' : 'Jerry',
           'location': 'San Diego',
           'password': 'qwerty123456' }
data = urllib.urlencode(values)
request = urllib2.Request(url, data)
try:
    response = urllib2.urlopen(request)
    read_page = response.read()
    print read_page
except urllib2.URLError, e:
    print 'reason', e.reason
    #print 'code', e.code

# Get method of http request
data = {}
data['name'] = 'Jerry'
data['location'] = 'San Diego'
data['password'] = 'qwerty123456'

request_values = urllib.urlencode(data)
print request_values

url = 'http://www.server.come/register.jsp'
full_url = url + '?' + request_values
print full_url
try:    
    response = urllib2.urlopen(full_url)
    read_page = response.read()
    print read_page
except urllib2.URLError, e:
    print 'reason', e.reason
    #print 'code', e.code

# Recommended way to hanlde exception/error
request = urllib2.Request('http://www.server.come/register.jsp')
try:
    responed = urllib2.urlopen(request)
except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print 'Error code:', e.code
    if hasattr(e,' reason'):
        print 'Failure reason:', e.reason
else:
    print 'No exception was raised'


# info() & geturl()
url = 'http://www.google.com/'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
print 'Real url:', response.geturl()
print 'Info'
print response.info()