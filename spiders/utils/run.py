from typing import *

from spiders.base import BaseSpider
from spiders.dummy import Dummy
from spiders.utils.base_logger import logger


def get_spider_list() -> List:
    return [
        Dummy
    ]


def run(spiders: Optional[List[BaseSpider or type]] = None):
    spiders = spiders if spiders is not None else get_spider_list()
    for s in spiders:
        spider: BaseSpider = s
        if not isinstance(s, BaseSpider):
            # logger.info(f"create spider from {spider}")
            spider = s()
            # logger.info(f"spider = {spider}")
        logger.info(f"Spider {spider.name} start")
        spider.run()
        logger.info(f"Spider {spider.name} done")
