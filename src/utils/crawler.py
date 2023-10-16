import re
import json
import requests
import logging
import random
from bs4 import BeautifulSoup
from src.utils.logger import *
from src.utils.wbi_encoder import *

class Crawler(object):
    '爬虫的基类'
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
        }
        self.logger = getLogger(__name__)
        self.wbiEncoder = WbiEncoder()
    
    def getPage(self, url, params = None):
        '获取网页源代码'
        try:
            html = self.session.get(url, params=params)
            html.raise_for_status()
            html.encoding = html.apparent_encoding
            self.logger.debug('html encoding: {}'.format(html.encoding))
            self.logger.info('success to get html from {}'.format(url))
            return html.text
        except:
            self.logger.error('fail to get html from {}'.format(url))
            return ''
    