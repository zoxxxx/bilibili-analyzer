from src.utils import *
import time
class UserCrawler(Crawler):
    '爬取bilibili用户信息'
    def __init__(self, mid):
        super().__init__()
        self.mid = mid
    
    def getVideos(self):
        '获取用户所有视频'
        url = 'https://api.bilibili.com/x/space/wbi/arc/search'
        self.logger.debug('start to get videos from user {}'.format(self.mid))
        self.time = time.time()
        i = 1
        while True:
            params = {
                'mid': self.mid,
                'ps': 50,
                'tid': 0,
                'pn': i,  # 第几页
                'keyword': '',
                'order': 'pubdate',
                'platform': 'web',
                'order_avoided': 'true',
            }
            html = self.getPage(url, params=params)
            load = json.loads(html) 
            if load['code'] != 0:
                self.logger.error('fail to get videos from user {} page {}, error code = {}'.format(self.mid, i, load['code']))
                break
            videos = load['data']['list']['vlist']
            if len(videos) == 0:
                break
            i += 1
            for video in videos:
                yield video
        self.logger.debug('success to get videos from user {}'.format(self.mid))
    
    def getUserInfo(self):
        '获取用户基本信息'
        url = 'https://api.bilibili.com/x/space/wbi/acc/info'
        self.logger.debug('start to get user info from user {}'.format(self.mid))
        params = {
            'mid': self.mid
        }
        signedParams = self.wbiEncoder.getSignedParams(params)
        html = self.getPage(url, params=signedParams)
        load = json.loads(html)
        if load['code'] != 0:
            self.logger.error('fail to get user info from user {}, error code = {}'.format(self.mid, load['code']))
            return None
        self.logger.debug('success to get user info from user {}'.format(self.mid))
        return load['data']
    
    def getData(self):
        data = self.getUserInfo()
        videos = []
        for video in self.getVideos():
            videos.append(video)
        data['videos'] = videos
        return data