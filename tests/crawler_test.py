from src import *

if __name__ == "__main__":
    logger = getLogger(__name__)
    userCrawler = UserCrawler(546195)
    logger.debug(userCrawler.getMid("泛式"))
    