# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import cookielib
import sys
import time
import requests

my_pixiv_id = 'scraper4f@gmail.com'
my_password = 'scraper123'
#sess = requests.session()

# Build opener that records cookies
cookie = cookielib.CookieJar()
auth_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
other_opener 

def retrieve_post_key():
    print 'Retrieving post key...'
    key_url = 'https://accounts.pixiv.net/login?lang=en&source=pc&view_type=page&ref=wwwtop_accounts_index'
    key_header = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Host' : 'accounts.pixiv.net',
        'Connection' : 'keep-alive'
    }

    request = urllib2.Request(url=key_url, headers=key_header)
    try:
        response = auth_opener.open(key_url)
        read_page = response.read()
    except IOError, e:
        print '\x1b[1;31;40m' + 'failed: something went wrong' + '\x1b[0m'
        if hasattr(e, 'code'):
            print '     error code: ', e.code
        if hasattr(e, 'reason'):
            print '     failure reason: ', e.reason
        sys.exit()
    else:
        key_pattern = re.compile(r'"pixivAccount.postKey":"([\d|\w]+)"')
        key_match = key_pattern.search(read_page)

        if key_match:
            print '\x1b[1;32;40m' + 'key found' + '\x1b[0m'
            return key_match.group(1)
        else:
            print '\x1b[1;31;40m' + 'failed: no match found' + '\x1b[0m'
            sys.exit()
    '''
    response = sess.get(key_url, headers=key_header)
    read_page = response.text
    key_pattern = re.compile(r'"pixivAccount.postKey":"([\d|\w]+)"')
    key_match = key_pattern.search(read_page)

    if key_match:
        print '\x1b[1;32;40m' + 'key found' + '\x1b[0m'
        return key_match.group(1)
    else:
        print '\x1b[1;31;40m' + 'failed: no match found' + '\x1b[0m'
        sys.exit()    
    '''

def account_login(post_key, pixiv_id=my_pixiv_id, password=my_password):
    login_url = 'https://accounts.pixiv.net/api/login?lang=en'
    login_value = {
        'pixiv_id' : pixiv_id,
        'password' : password,
        'captcha' : '',
        'g_recaptcha_response' : '',
        'post_key' : post_key,
        'source' : 'pc',
        'ref' : 'wwwtop_accounts_index',
        'return_to' : 'https://www.pixiv.net/',
    }
    login_data = urllib.urlencode(login_value)
    login_header = {
        'Referer' : 'https://accounts.pixiv.net/login?lang=en&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Connection' : 'keep-alive',
        'Host' : 'accounts.pixiv.net'
    }

    request = urllib2.Request(url=login_url, data=login_data, headers=login_header)
    try:
        response = auth_opener.open(request, timeout=20)
        read_page = response.read()
    except IOError, e:
        print '\x1b[1;31;40m' + 'login failed' + '\x1b[0m'
        if hasattr(e, 'code'):
            print '     error code: ', e.code
        if hasattr(e, 'reason'):
            print '     failure reason: ', e.reason
        sys.exit()
    else:
        print read_page

    #response = sess.post(login_url, data=login_value, headers=login_header)

def main():
    post_key = retrieve_post_key()
    account_login(post_key=post_key)

    home_header = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Host' : 'accounts.pixiv.net',
        'Connection' : 'keep-alive'
    }
    home_url = 'https://www.pixiv.net/search.php?s_mode=s_tag&word=NieR'
    response = sess.get(home_url, headers=home_header)
    print response.text

if __name__ == '__main__':
    main()