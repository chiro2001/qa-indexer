from spiders.base import *


class Dfzq(StaticSpider):
    NAME = "东方证券"

    def __init__(self):
        super().__init__(Dfzq.NAME, "FAQ _ 東方金融控股（香港）有限公司.html")

    def parse_html(self, html: str) -> List[QaItem]:
        soup = Soup(html, "html.parser")
        qa_box = soup.select_one('div[class="inner-box"]')
        classifications = qa_box.select('div[class="item"]')
        qa: List[QaItem] = []
        for classification in classifications:
            classification_name = classification.select_one('div[class="title"]').get_text().strip()
            logger.info(classification_name)

            def parse_qa_item(item: Soup) -> QaItem:
                q: str = item.select_one('dt').get_text().strip()
                q = q[1:] if q.startswith('问') else q
                return QaItem(
                    question=q,
                    answer=str(item.select_one('dd')) if self.html_out else item.select_one('dd').get_text().strip(),
                    other={
                        "classification": classification_name
                    }
                )

            qa.extend([parse_qa_item(dl) for dl in classification.select('dl')])
        return qa
