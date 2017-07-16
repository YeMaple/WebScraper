# -*- coding: utf-8 -*-

import urllib2
import re

def retrieve_from_page(page):
    # http_pattern = re.compile(r'<span><li>(\d*.\d*.\d*.\d*)</li></span>')
    http_pattern = re.compile(r'<td>(\d+.\d+.\d+.\d+)</td>')
    port_pattern = re.compile(r'<td>(\d+)</td>')
    type_pattern = re.compile(r'<td>(HTTP|HTTPS|socks4/5)</td>')

    https = []
    ports = []
    types = []

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
    return https, ports, types

def retrieve_from_url(url=None):
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

def test_proxy(proxy_http, proxy_port, proxy_type):
    proxy_handler = urllib2.ProxyHandler({})
    return True

def main():
    proxy_https, proxy_ports, proxy_types = retrieve_from_url()
    for i in range(len(proxy_https)):
        print test_proxy(proxy_https[i], proxy_ports[i], proxy_types[i])


if __name__ == '__main__':
    main() 