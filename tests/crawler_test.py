from src import *

if __name__ == "__main__":
    logger = getLogger(__name__)
    videoData = VideoData("BV1sm4y1g7iM")
    videoData.update()
    logger.debug(videoData.getData())
    