from src.utils import *
from src.crawler.user_crawler import *
import os
class UserData(Data):
    def __init__(self, mid = None, name = None):
        super().__init__()
        self.crawler = UserCrawler(mid=mid, name=name)
        self.mid = self.crawler.mid
        self.data = []
        self.path = 'data/users/{}.json'.format(self.mid)
        if os.path.exists(self.path):
            self.load()
            self.loaded = True
    
        