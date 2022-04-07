from spiders.utils.base_logger import logger

__all__ = ['dummy', 'utils', 'get_spider_list', 'Dummy', 'logger']

from spiders import utils
from spiders.base import BaseSpider
from spiders.utils import *
from typing import *

from spiders.dummy import Dummy


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
