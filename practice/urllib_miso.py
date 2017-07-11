import urllib2
import cookielib

# Get cookie
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open('http://www.google.com')

for item in cookie:
    print 'Name: ', item.name
    print 'Value: ', item.value

# Proxy setting
proxy_handler = urllib2.ProxyHandler({"http" : '12.184.129.132:8080'})
opener = urllib2.build_opener(proxy_handler)
response = opener.open('http://www.baidu.com')

read_page = response.read()
print read_page

# Header
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer' : 'http://www.baidu.com'
}

request = urllib2.Request(
    url = 'http://www.baidu.com',
    headers = headers
    )
response = urllib2.urlopen(request)
read_page = response.read()
print read_page