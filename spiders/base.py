import json
import os.path
from abc import *
from datetime import timedelta
from functools import reduce
from typing import *
import bs4
from bs4 import BeautifulSoup as Soup
from requests_cache import CachedSession
from tqdm import trange

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
        self.out_file = os.path.join('data', out_file if out_file is not None else f"{name}.json")
        self.html_out = html_out

    @abstractmethod
    def fetch_page_count(self) -> int:
        """
        :return: 页面总数
        """
        pass

    @abstractmethod
    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
        """
        解析 html 到 QA List
        :param html: html 文本
        :return: QA List
        """
        pass

    @abstractmethod
    def fetch_page_content(self, page: Optional[int] = None) -> str:
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

    def fetch_page(self, **kwargs) -> List[QaItem]:
        html = self.fetch_page_content(self.page_now)
        data = self.parse_content(html, **kwargs)
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
        logger.info(f"run with {self.page_max} pages")
        # while not self.is_finish():
        for page_ in trange(self.page_max):
            retry_now = self.retry
            while retry_now > 0:
                try:
                    qa_list = self.fetch_page(page=self.page_now)
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
    def __init__(self,
                 name: str,
                 filename: str,
                 path: str = 'dataset/data-from-internet/static',
                 **kwargs):
        super().__init__(name, **kwargs)
        self.filename = filename
        self.path = path

    @abstractmethod
    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
        pass

    def fetch_page_count(self) -> int:
        return 1

    def fetch_page_content(self, page: int = None) -> str:
        with open(os.path.join(self.path, self.filename), "r", encoding="utf8") as f:
            return f.read()


class WebSpider(BaseSpider):
    def __init__(self, name: str):
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36"
        self.session = WebSpider.get_cached_session()
        super().__init__(name)

    @abstractmethod
    def get_cookie(self) -> str:
        pass

    def request(self, url: str, method: str = 'GET', *args, **kwargs):
        headers = {
            "Cookie": self.get_cookie(),
            "User-Agent": self.ua
        }
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']
        return self.session.request(method, url, headers=headers, *args, **kwargs)

    @staticmethod
    def get_cached_session(name: str = 'spider_cache'):
        return CachedSession(
            os.path.join(os.path.join(os.environ.get('userprofile', '~'), '.requests_cache'), name),
            use_cache_dir=True,  # Save files in the default user cache dir
            cache_control=False,  # Use Cache-Control headers for expiration, if available
            expire_after=timedelta(days=30),  # Otherwise, expire responses after one day
            allowable_methods=['GET', 'POST'],
            # Cache POST requests to avoid sending the same data twice
            allowable_codes=[200, 400],  # Cache 400 responses as a solemn reminder of your failures
            ignored_parameters=['api_key', '.pdf'],  # Don't match this param or save it in the cache
            match_headers=False,  # Match all request headers
            stale_if_error=True  # In case of request errors, use stale cache data if possible)
        )
