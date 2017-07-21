# -*- coding: utf-8 -*-

import re
import os
import sys
import datetime
import time
import requests
import argparse
from bs4 import BeautifulSoup

my_pixiv_id = 'scraper4f@gmail.com'
my_password = 'scraper123'
sess = requests.session()

def mkdir_if_not_exists(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

def create_download_folder(get_recommend, get_top, search_key_word, main_dir='./pixiv'):
    curr_time = time.time()
    timestamp = datetime.datetime.fromtimestamp(curr_time).strftime('%Y%m%d_%H:%M:%S')

    sess_dir = os.path.join(main_dir, my_pixiv_id + '_' + timestamp)
    mkdir_if_not_exists(main_dir)
    mkdir_if_not_exists(sess_dir)

    recommend_dir, top_dir, search_dir = None, None, None

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
        print e
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
    post_key = retrieve_post_key()

    print 'Login to pixiv account...'
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
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0'
    }

    try:
        response = sess.post(login_url, data=login_form, headers=login_header)
    except IOError, e:
        print '\x1b[1;31;40m' + 'login failed' + '\x1b[0m'
        sys.exit()
    else:
        print '\x1b[1;32;40m' + 'login success' + '\x1b[0m'

def extract_image_from_url(image_url, target_dir):
    print 'Extracting image... from ', image_url
    image_header = {
        'Referer' : 'https://www.pixiv.net/',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0'   
    }

    try:
        response = sess.get(image_url, headers=image_header)
    except IOError, e:
        print '\x1b[1;31;40m' + 'cannot access image page' + '\x1b[0m'
        return
    else:
        read_page = BeautifulSoup(response.content, 'lxml')

    # Extract image source url
    image_div = read_page.find('div', class_='works_display')
    if image_div:
        image_src = image_div.find('img').get('src')
    else:
        print '\x1b[1;33;40m' + 'no images found on page' + '\x1b[0m'
        return
    
    save_name = image_src.split('/')[-1]
    image_file = os.path.join(target_dir, save_name)

    try:
        with open(image_file, 'wb+') as f:
            f.write(sess.get(image_src, headers=image_header).content)
        f.close()

    except Exception, e:
        print 'Downloading image file: ', save_name, '\x1b[1;31;40m' + ' -- download failed' + '\x1b[0m'
    else:
        print 'Downloading image file: ', save_name, '\x1b[1;32;40m' + ' -- download success' + '\x1b[0m'

def download_recommend(target_dir):
    print 'Downloading recommended illusts'

    recommend_main_url = 'https://www.pixiv.net/recommended.php'
    recommend_main_header = {
        'Referer' : 'https://www.pixiv.net/',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
    }

    try:
        response = sess.get(recommend_main_url, headers=recommend_main_header)
    except IOError, e:
        print '\x1b[1;31;40m' + 'cannot access recommend page' + '\x1b[0m'
        print e
        return
    else:
        read_page = BeautifulSoup(response.content, 'lxml')

    hidden_tt = read_page.find('input', {'name' : 'tt'}).get('value')

    recommend_get_url = 'https://www.pixiv.net/rpc/recommender.php'
    recommend_get_header = {
        'Referer' : 'https://www.pixiv.net/recommended.php',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Connection' : 'keep-alive'
    }
    recommend_get_form = {
        'type' : 'illust',
        'sample_illusts' : 'auto',
        'num_recommendations' : '500',
        'tt' : hidden_tt
    }

    try:
        response = sess.get(recommend_get_url, 
                            headers=recommend_get_header, 
                            params=recommend_get_form)
    except IOError, e:
        print '\x1b[1;31;40m' + 'cannot get recommendations' + '\x1b[0m'
        print e
        return
    else:
        read_page = response.json()

    image_base_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'
    for illust_id in read_page['recommendations']:
        image_url = image_base_url.format(illust_id)
        extract_image_from_url(image_url, target_dir)
        time.sleep(3)

def download_top(target_dir):
    print 'Downloading top illusts'

    home_url = 'https://www.pixiv.net/'
    top_url = 'https://www.pixiv.net/ranking_area.php?type=detail&no=6'
    try:
        response = sess.get(top_url)
    except IOError, e:
        print '\x1b[1;31;40m' + 'cannot access top page' + '\x1b[0m'
        print e
        return
    else:
        read_page = BeautifulSoup(response.content, 'lxml')

    top_div = read_page.find_all('div', class_='ranking-item')
    for div in top_div:
        urls = div.find_all('a')
        image_url = home_url + urls[1].get('href')
        extract_image_from_url(image_url, target_dir)
        time.sleep(3)

def download_search(key_word,target_dir):
    print 'Searching key word {}'.format(key_word)

    home_url = 'https://www.pixiv.net/'
    search_url = 'https://www.pixiv.net/search.php'
    search_header = {
        'Referer' : 'https://www.pixiv.net/',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Connection' : 'keep-alive'
    }
    search_form = {
        's_mode': 's_tag',
        'word' : key_word
    }

    try:
        response = sess.get(search_url,
                            headers=search_header,
                            params=search_form)
    except IOError, e:
        print '\x1b[1;31;40m' + 'cannot access search page' + '\x1b[0m'
        print e
        return
    else:
        read_page = BeautifulSoup(response.content, 'lxml')

    search_section = read_page.find('section', class_='column-search-result')
    image_list = search_section.find_all('li', class_='image-item')
    for item in image_list:
        urls = item.find_all('a')
        image_url = home_url + urls[1].get('href')
        extract_image_from_url(image_url, target_dir)
        time.sleep(3)

    
def main(get_recommend, get_top, search_key_word):
    # Prepare folder for downloading
    recommend_dir, top_dir, search_dir = create_download_folder(get_recommend, get_top, search_key_word)

    # Session login
    login()

    # Download
    if get_recommend:
        download_recommend(recommend_dir)
        time.sleep(5)

    if get_top:
        download_top(top_dir)
        time.sleep(5)

    if search_key_word:
        download_search(search_key_word, search_dir)
        time.sleep(5)

    sess.close()

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
        print '\x1b[1;33;40m' + 'no flags have been set, default to download top' + '\x1b[0m'
        results.top = True

    main(results.recommend, results.top, results.search_key_word)