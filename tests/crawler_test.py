from src import *

if __name__ == "__main__":
    logger = getLogger(__name__)
    userData = UserData("406636263")
    userData.download()
    userData.update()
    data  = userData.getData()