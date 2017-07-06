import urllib
import urllib2

'''
response = urllib2.urlopen('http://www.google.com/')
html = response.read()
print html
'''

'''
request = urllib2.Request('http://www.google.com/')
response = urllib2.urlopen(request)
read_page = response.read()
print read_page
'''

# Post method of http request
url = 'http://www.server.come/register.jsp'
values = { 'name' : 'Jerry',
           'location': 'San Diego',
           'password': 'qwerty123456' }
data = urllib.urlencode(values)
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
read_page = response.read()

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
response = urllib2.open(full_url)
