import json
import os.path
from abc import *
from functools import reduce
from typing import *
from bs4 import BeautifulSoup as Soup

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
                 retry: int = 3,
                 out_file: str = None,
                 html_out: bool = True):
        """
        基础爬虫类
        :param name:        爬虫名称
        :param page_start:  开始页
        :param retry:       重试次数
        :param out_file:    输出文件名
        :param html_out:    是否以`html`格式输出
        """
        self.name = name
        self.page_now = page_start
        self.page_max = self.fetch_page_count()
        self.database = {}
        self.retry = retry
        self.out_file = out_file if out_file is not None else f"data/{name}.json"
        self.html_out = html_out

    @abstractmethod
    def fetch_page_count(self) -> int:
        """
        :return: 页面总数
        """
        pass

    @abstractmethod
    def parse_html(self, html: str) -> List[QaItem]:
        """
        解析 html 到 QA List
        :param html: html 文本
        :return: QA List
        """
        pass

    @abstractmethod
    def fetch_page_html(self, page: Optional[int] = None) -> str:
        """
        按页面获取 html
        :param page:    页面
        :return: html   文本
        """
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
        self.storage_sync()

    def format_database(self) -> List[QaItem]:
        return reduce(lambda x, y: x + y, [[d.__dict__ for d in self.database[key]] for key in self.database])

    def storage_sync(self):
        with open(self.out_file, "w", encoding="utf8") as f:
            json.dump(self.format_database(), f, ensure_ascii=False, indent=2)

    def add_extra_data(self, qa: QaItem) -> QaItem:
        qa.other = {} if qa.other is None else qa.other
        qa.other["source"] = self.name
        return qa

    def run(self):
        logger.info("run")
        while not self.is_finish():
            retry_now = self.retry
            while retry_now > 0:
                try:
                    qa_list = self.fetch_page()
                    qa_list = [self.add_extra_data(qa) for qa in qa_list]
                    self.save_data(qa_list)
                    break
                except Exception as e:
                    retry_now -= 1
                    logger.warning(f"Except: {e} ({type(e)}), retry remains {retry_now}")
                    if retry_now <= 0:
                        raise e
            self.to_next_page()


class StaticSpider(BaseSpider):
    def __init__(self, name: str, filename: str, path: str = 'dataset/data-from-internet/static'):
        super().__init__(name)
        self.filename = filename
        self.path = path

    @abstractmethod
    def parse_html(self, html: str) -> List[QaItem]:
        pass

    def fetch_page_count(self) -> int:
        return 1

    def fetch_page_html(self, page: int = None) -> str:
        with open(os.path.join(self.path, self.filename), "r", encoding="utf8") as f:
            return f.read()
