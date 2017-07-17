# -*- coding: utf-8 -*-

import urllib2
import re
import time

def test_proxy(proxy_http, proxy_port, proxy_type):
    print 'Testing acquired proxy...'
    proxy_handler = urllib2.ProxyHandler({proxy_type.lower() : proxy_http + ':' + proxy_port})
    opener = urllib2.build_opener(proxy_handler)
    test_url = 'http://ip.chinaz.com/'

    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer' : 'http://www.xicidaili.com/'    
    } 
    request = urllib2.Request(
        url=test_url,
        headers=header
        )
    try:
        response = opener.open(test_url, timeout=10)
        read_page = response.read()
    except IOError, e:
        print '\x1b[1;31;40m' + 'test failed: something went wrong' + '\x1b[0m'
        if hasattr(e, 'code'):
            print '     error code: ', e.code
        if hasattr(e, 'reason'):
            print '     failure reason: ', e.reason
        return False
    else:
        ip_pattern = re.compile(r'<dd class="fz24">(\d+.\d+.\d+.\d+)</dd>')
        ip_match = ip_pattern.search(read_page)

        if ip_match:
            if ip_match.group(1) == proxy_http:
                print '\x1b[1;32;40m' + 'test passed: proxy is usable' + '\x1b[0m'
                return True
            else:
                print '\x1b[1;31;40m' + 'test failed: proxy is not usable' + '\x1b[0m'
                print '     acutual ip: ', ip_match.group(1)
                print '     expected ip: ', proxy_http
                return False
        else:
            print '\x1b[1;31;40m' + 'test failed: no match found' + '\x1b[0m'
            print '     no match found'
            return False

def retrieve_from_page(page):
    print 'Processing proxy webpages...'
    # http_pattern = re.compile(r'<span><li>(\d*.\d*.\d*.\d*)</li></span>')
    http_pattern = re.compile(r'<td>(\d+.\d+.\d+.\d+)</td>')
    port_pattern = re.compile(r'<td>(\d+)</td>')
    type_pattern = re.compile(r'<td>(HTTP|HTTPS|socks4/5)</td>')

    https = []
    ports = []
    types = []
    '''
    http_matches = http_pattern.findall(page)
    if http_matches:
        for item in http_matches:
            https.append(item)
    else:
        print 'no http address match found'

    port_matches = port_pattern.findall(page)
    if port_matches:
        for item in port_matches:
            ports.append(item)
    else:
        print 'no port number match found'

    assert len(https) == len(ports)

    type_matches = type_pattern.findall(page)
    if type_matches:
        for item in type_matches:
            types.append(item)
    else:
        print 'no type match found'

    assert len(https) == len(types)
    '''

    http_matches = http_pattern.findall(page)
    port_matches = port_pattern.findall(page)
    type_matches = type_pattern.findall(page)

    if not http_matches:
        print 'no http address match found'
    if not port_matches:
        print 'no port number match found'
    if not type_matches:
        print 'no type match found'

    for (h, p, t) in zip(http_matches, port_matches, type_matches):
        if not t.startswith('s'):
            if test_proxy(h, p, t):
                https.append(h)
                ports.append(p)
                types.append(t)

        time.sleep(2)
        if len(https) == 5:
            break

    return https, ports, types

def retrieve_from_url(url=None):
    print 'Retrieving proxy lists...'
    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer' : 'http://www.xicidaili.com/'    
    }
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    if url is None:
        proxy_url = 'http://www.xicidaili.com/'
    else:
        proxy_url = url
    request = urllib2.Request(
        url=proxy_url,
        headers=header
        )

    try:
        response = opener.open(request)
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print 'error code: ', e.code
        if hasattr(e, 'reason'):
            print 'failure reason: ', e.reason
    else:
        read_page = response.read()

    # print read_page
    return retrieve_from_page(read_page)

def main():
    proxy_https, proxy_ports, proxy_types = retrieve_from_url()

if __name__ == '__main__':
    main() 