from spiders.base import *


class Dummy(BaseSpider):
    NAME = "dummy"

    def __init__(self):
        super().__init__(Dummy.NAME)

    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
        logger.info("parsing html")
        return [QaItem("Q", "A"), ]

    def fetch_page_count(self) -> int:
        logger.info("fetching page count")
        return 1

    def fetch_page_content(self, page: int = None) -> str:
        logger.info(f"fetching html from page {page}")
        return ""
