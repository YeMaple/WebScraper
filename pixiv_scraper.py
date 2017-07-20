# -*- coding: utf-8 -*-

import re
import os
import sys
import datetime
import time
import requests
import argparse

my_pixiv_id = 'scraper4f@gmail.com'
my_password = 'scraper123'
sess = requests.session()

def mkdir_if_not_exists(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

def create_download_folder(get_recommend, get_top, search_key_word, main_dir='./pixiv'):
    curr_time = time.time()
    timestamp = datetime.datetime.fromtimestamp(curr_time).strftime('%Y%m%d_%H:%M:%S')

    sess_dir = os.path.join(main_dir, timestamp)
    mkdir_if_not_exists(main_dir)
    mkdir_if_not_exists(sess_dir)

    if get_recommend:
        recommend_dir = os.path.join(sess_dir, 'Recommend')
        mkdir_if_not_exists(recommend_dir)

    if get_top:
        top_dir = os.path.join(sess_dir, 'Top')
        mkdir_if_not_exists(top_dir)

    if search_key_word:
        search_dir = os.path.join(sess_dir, search_key_word)
        mkdir_if_not_exists(search_dir)

    return recommend_dir, top_dir, search_dir

def retrieve_post_key():
    print 'Retrieving post key...'
    key_url = 'https://accounts.pixiv.net/login?lang=en&source=pc&view_type=page&ref=wwwtop_accounts_index'
    key_header = {
        'Referer': 'https://www.pixiv.net/',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
    }

    try:
        response = sess.get(key_url, headers=key_header)
        read_page = response.text
    except IOError, e:
        print '\x1b[1;31;40m' + 'retrival failed: something went wrong' + '\x1b[0m'
        sys.exit()
    else:
        key_pattern = re.compile(r'"pixivAccount.postKey":"([\d|\w]+)"')
        key_match = key_pattern.search(read_page)

    if key_match:
        print '\x1b[1;32;40m' + 'retrival success: key found' + '\x1b[0m'
        return key_match.group(1)
    else:
        print '\x1b[1;31;40m' + 'retrival failed: no match found' + '\x1b[0m'
        sys.exit()    

def login(pixiv_id=my_pixiv_id, password=my_password):
    print 'Login to pixiv account'
    post_key = retrieve_post_key()

    login_url = 'https://accounts.pixiv.net/api/login'
    login_form = {
        'pixiv_id' : pixiv_id,
        'password' : password,
        'captcha' : '',
        'g_recaptcha_response' : '',
        'post_key' : post_key,
        'source' : 'pc',
        'ref' : 'wwwtop_accounts_index',
        'return_to' : 'https://www.pixiv.net/',
    }
    login_header = {
        'Referer' : 'https://accounts.pixiv.net/login?lang=en&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
    }

    try:
        response = sess.post(login_url, data=login_form, headers=login_header)
    except IOError, e:
        print '\x1b[1;31;40m' + 'login failed' + '\x1b[0m'
        sys.exit()
    else:
        print '\x1b[1;32;40m' + 'login success' + '\x1b[0m'

def download_recommend(target_dir):
    home_url = 'https://www.pixiv.net/'

def main(get_recommend, get_top, search_key_word):
    # Prepare folder for downloading
    recommend_dir, top_dir, search_dir = create_download_folder(get_recommend, get_top, search_key_word)

    # Session login
    login()

    if get_recommend:
        download_recommend(recommend_dir)



if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download options.')
    parser.add_argument('-r', '--recommend', action='store_true', dest='recommend',
                         help='download recommeded illusts')
    parser.add_argument('-t', '--top', action='store_true', dest='top',
                         help='download top 100 illusts')
    parser.add_argument('-s', '--search', action='store', dest='search_key_word',
                         help='search keyword', type=str)
    results = parser.parse_args()

    # If no flags are set, default to download top
    if not results.recommend and not results.top and results.search_key_word is None:
        results.top = True

    main(results.recommend, results.top, results.search_key_word)