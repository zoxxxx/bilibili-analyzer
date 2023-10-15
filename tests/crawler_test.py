from src import *

if __name__ == "__main__":
    print(1)
    logger = get_logger(__name__)
    crawler = UserCrawler('546195')
    for video in crawler.getVideos():
        logger.debug(video)
    # logger.debug(html)
    # logger.debug(crawler.get_html('https://www.bilibili.com/video/BV1sm4y1g7iM/'))