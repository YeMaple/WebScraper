# WebScraper
A web scraper that downloads downloads top 100/recommended/keyword searching illusts from [pixiv](https://www.pixiv.net/)

## Dependencies
* Python (2.7.13)
* bs4 (4.6.0)
* lxml (3.8.0)

Please use pip to install dependencies
`pip install <name>` or `sudo pip install <name>`

## Usage
**python pixiv_scraper.py --help**

```
usage: pixiv_scraper.py [-h] [-r] [-t] [-s SEARCH_KEY_WORD]

Download options.

optional arguments:
  -h, --help            show this help message and exit
  -r, --recommend       download recommeded illusts
  -t, --top             download top 100 illusts
  -s SEARCH_KEY_WORD, --search SEARCH_KEY_WORD
                        search keyword
```

## TODO
...