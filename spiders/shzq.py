from typing import Optional

from spiders.base import *


class Shzq(StaticSpider):
    NAME = "上海证券"

    def __init__(self):
        super().__init__(Shzq.NAME, "IPO常见问题 _ 上海证券交易所.html")

    def parse_html(self, html: str) -> List[QaItem]:
        soup = Soup(html, "html.parser")
        qa: List[QaItem] = []
        classification_name = "IPO常见问题"
        qa_box = soup.select_one('div[class="sse_list_6"]')

        def parse_item(item) -> Optional[QaItem]:
            if isinstance(item, str):
                return None
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

        qa.extend(filter(lambda x: x is not None, [parse_item(item) for item in qa_box.find_all("li")]))
        return qa
