from src.utils import *
from src.crawler.user_crawler import *
import os
class UserData(Data):
    def __init__(self, mid):
        super().__init__()
        self.mid = mid
        self.data = []
        self.crawler = UserCrawler(self.mid)
        self.path = 'data/users/{}.json'.format(self.mid)
        if os.path.exists(self.path):
            self.load()
            self.loaded = True
    
        