from src import *

if __name__ == "__main__":
    logger = getLogger(__name__)
    crawler = Crawler()
    # url = 'https://api.bilibili.com/x/space/arc/search?mid=19577966&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
    url = 'https://api.bilibili.com/x/space/wbi/arc/search'
    mid = '406636263'
    params = {
        'mid': mid,
        'ps': 50,
        'tid': 0,
        'pn': 1,  # 第几页
        'keyword': '',
        'order': 'pubdate',
        'platform': 'web',
        # 'web_location': '1550101',
        'order_avoided': 'true',
    }

    html = crawler.getPage(url, params=params)
    logger.debug(html)
    # logger.debug(crawler.get_html('https://www.bilibili.com/video/BV1sm4y1g7iM/'))