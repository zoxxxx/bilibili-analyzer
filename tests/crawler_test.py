from src import *

if __name__ == "__main__":
    logger = getLogger(__name__)
    videoCrawler = VideoCrawler('BV1H84y127ym')
    logger.info(videoCrawler.getData())
    