from src.utils import *
class VideoCrawler(Crawler):
    def __init__(self, bvid):
        super().__init__()
        self.bvid = bvid
    
    def getVideoArchive(self):
        url = 'https://api.bilibili.com/x/web-interface/archive/stat'
        params = {
            'bvid': self.bvid
        }
        html = self.getPage(url, params=params)
        self.logger.debug(html)
        load = json.loads(html)
        if load['code'] != 0:
            self.logger.error('fail to get video archive from video {}, error code = {}'.format(self.bvid, load['code']))
            return None
        return load['data']
    
    def getData(self):
        data = self.getVideoArchive()
        return data
