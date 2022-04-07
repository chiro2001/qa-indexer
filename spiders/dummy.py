from typing import *
from spiders.base import BaseSpider, QaItem


class Dummy(BaseSpider):
    NAME = "dummy"

    def __init__(self):
        super().__init__(Dummy.NAME)

    def parse_html(self, html: str) -> List[QaItem]:
        return [QaItem("Q", "A"), ]

    def fetch_page_count(self) -> int:
        return 0

    def fetch_page_html(self, page: int = None) -> str:
        return ""
