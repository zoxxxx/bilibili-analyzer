from src.utils.logger import *
import json
import datetime
import os
class Data(object):
    '数据基类'
    def __init__ (self):
        self.logger = getLogger(__name__)
        self.loaded = False
        self.data = None
        self.time = None
        self.path = None
        self.crawler = None
    
    def download(self):
        if self.loaded:
            self.logger.warning("already downloaded, try update")
            return
        self.time = datetime.datetime.now()
        self.loaded = True
        self.data = self.crawler.getData()
        self.save()

    def update(self):
        self.logger.info("update data")
        self.time = datetime.datetime.now()
        self.loaded = True
        self.data = self.crawler.getData()
        self.save()

    def save(self):
        self.logger.info('start to save {}'.format(self.path))
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            self.logger.error('fail to save {}'.format(self.path))
            return
        self.logger.info('success to save {}'.format(self.path))
    
    def load(self):
        self.logger.info('start to load {}' + self.path)
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.logger.error('fail to load {}'.format(self.path))
            return
        self.logger.info('success to load {}'.format(self.path))

    def getData(self):
        if not os.path.exists(self.path):
            self.download()
        elif not self.loaded:
            self.load()
        return self.data