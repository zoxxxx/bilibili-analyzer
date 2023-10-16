import os
from src.utils import *
from src.crawler.video_crawler import *
class VideoData(Data):
    def __init__(self, bvid):
        super().__init__()
        self.bvid = bvid
        self.data = []
        self.crawler = VideoCrawler(self.bvid)
        self.path = 'data/videos/{}.json'.format(self.bvid)
        if os.path.exists(self.path):
            self.load()
            self.loaded = True