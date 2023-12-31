from src.utils import *
class VideoCrawler(Crawler):
    def __init__(self, bvid):
        super().__init__()
        self.bvid = bvid
    
    def getVideoArchive(self):
        url = 'https://api.bilibili.com/x/web-interface/wbi/view/detail'
        params = {
            'bvid': self.bvid
        }
        signedParams = self.wbiEncoder.getSignedParams(params)
        html = self.getPage(url, params=signedParams)
        load = json.loads(html)
        if load['code'] != 0:
            self.logger.error('fail to get video archive from video {}, error code = {}'.format(self.bvid, load['code']))
            return None
        return load['data']['View']
    
    def getData(self):
        data = self.getVideoArchive()
        data.pop('ugc_season', None)
        return data
