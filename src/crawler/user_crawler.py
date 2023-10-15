from src.utils import *
class UserCrawler(Crawler):
    '爬取bilibili用户信息'
    def __init__(self, mid):
        super().__init__()
        self.mid = mid
    
    def getVideos(self):
        '获取用户所有视频'
        url = 'https://api.bilibili.com/x/space/wbi/arc/search'
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
                # 'web_location': '1550101',
                'order_avoided': 'true',
            }
            html = self.getPage(url, params=params)
            load = json.loads(html) 
            if load['code'] != 0:
                self.logger.error('fail to get videos from user {} page {}'.format(self.mid, i))
                break
            videos = load['data']['list']['vlist']
            if len(videos) == 0:
                break
            i += 1
            for video in videos:
                yield video