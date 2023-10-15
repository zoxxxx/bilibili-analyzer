import logging
def get_logger(__name__):
    '设置日志'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    FORMAT = "%(levelname)s: [%(asctime)s %(filename)s->%(funcName)s():%(lineno)s] %(message)s"
    formatter = logging.Formatter(FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler('.log', mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
