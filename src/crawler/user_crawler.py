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
                self.logger.error('fail to get videos from user {} page {}, error code = {}'.format(self.mid, i), load['code'])
                break
            videos = load['data']['list']['vlist']
            if len(videos) == 0:
                break
            i += 1
            for video in videos:
                yield video
        self.logger.debug('success to get videos from user {}'.format(self.mid))
    
    def getData(self):
        data = []
        for video in self.getVideos():
            data.append(video)
        return data