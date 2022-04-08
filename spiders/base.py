from abc import abstractmethod, ABC
from typing import *

from spiders.utils.base_logger import logger


class QaItem:
    def __init__(self,
                 question: str,
                 answer: str,
                 other: Optional[Any] = None):
        self.question = question
        self.answer = answer
        self.other = other


class BaseSpider(ABC):
    def __init__(self,
                 name: str,
                 page_start: int = 0,
                 retry: int = 3):
        self.name = name
        self.page_now = page_start
        self.page_max = self.fetch_page_count()
        self.database = {}
        self.retry = retry

    @abstractmethod
    def fetch_page_count(self) -> int:
        pass

    @abstractmethod
    def parse_html(self, html: str) -> List[QaItem]:
        pass

    @abstractmethod
    def fetch_page_html(self, page: int = None) -> str:
        pass

    def is_finish(self) -> bool:
        return self.page_now >= self.page_max

    def to_next_page(self):
        self.page_now = (self.page_now + 1) if not self.is_finish() else self.page_max

    def fetch_page(self) -> List[QaItem]:
        html = self.fetch_page_html(self.page_now)
        data = self.parse_html(html)
        return data

    def save_data(self, data: List[QaItem]):
        self.database[self.page_now] = data

    def run(self):
        logger.info("run")
        while not self.is_finish():
            retry_now = self.retry
            while retry_now > 0:
                try:
                    data = self.fetch_page()
                    self.save_data(data)
                    break
                except Exception as e:
                    retry_now -= 1
                    logger.warning(f"Except: {e} ({type(e)}), retry remains {retry_now}")
            self.to_next_page()


class StaticSpider(BaseSpider):
    def __init__(self, name: str):
        super().__init__(name)

    def fetch_page_count(self) -> int:
        pass

    def parse_html(self, html: str) -> List[QaItem]:
        pass

    def fetch_page_html(self, page: int = None) -> str:
        pass
