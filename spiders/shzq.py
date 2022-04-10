from spiders.base import *


class Shzq(StaticSpider):
    NAME = "上海证券"

    def __init__(self, *args, **kwargs):
        super().__init__(ShzqIPO.NAME, *args, **kwargs)

    def parse_item(self, item, classification_name: str) -> Optional[QaItem]:
        q: str = item.select_one('div[class="title"]').get_text().strip()
        q = q[q.find('：') + 1:]
        a = item.select_one('div[class="title-details2"]')
        return QaItem(
            question=q,
            answer=str(a) if self.html_out else a.get_text().strip(),
            other={
                "classification": classification_name
            }
        )

    @abstractmethod
    def parse_html(self, html: str) -> List[QaItem]:
        pass


class ShzqIPO(Shzq):
    def __init__(self):
        super().__init__("IPO常见问题 _ 上海证券交易所.html", out_file=f"{ShzqIPO.NAME}-IPO.json")

    def parse_html(self, html: str) -> List[QaItem]:
        soup = Soup(html, "html.parser")
        qa: List[QaItem] = []
        classification_name = "IPO常见问题"
        qa_box = soup.select_one('div[class="sse_list_6"]')

        qa.extend(
            [self.parse_item(item, classification_name) for item in qa_box.find_all("li") if not isinstance(item, str)])
        return qa


class ShzqInvestors(Shzq):
    def __init__(self):
        super().__init__("公众咨询服务热线常见问题 _ 上海证券交易所.html", out_file=f"{ShzqIPO.NAME}-Investors.json")

    def parse_html(self, html: str) -> List[QaItem]:
        soup = Soup(html, "html.parser")
        qa: List[QaItem] = []
        qa_box = soup.select_one('div[class="sse_wrap_cn_con"]')
        for sub_box in qa_box.select('div[class="sse_common_second_cn"]'):
            classification_name = sub_box.select_one('div[class="sse_subtitle_1"]').get_text().strip()
            qa.extend([self.parse_item(item, classification_name) for item in sub_box.find_all("li") if
                       not isinstance(item, str)])

        return qa
