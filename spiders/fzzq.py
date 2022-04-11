from spiders.base import *


class Fzzq(StaticSpider):
    NAME = "方正证券"

    def __init__(self):
        super().__init__(Fzzq.NAME, "方正证券-资讯.html")

    def parse_html(self, html: str) -> List[QaItem]:
        soup = Soup(html, "html.parser")
        qa: List[QaItem] = []
        qa_box = soup.select_one('div[class="k-infor_d-3"]')
        classification_name = "交易常见问题"
        strong_list = qa_box.select('strong')
        parent = strong_list[0].parent.parent
        question_box_list = [strong_list[i].parent for i in range(0, len(strong_list), 2)]
        question_box_index_list = [q.parent.index(q) for q in question_box_list]
        children = list(parent.children)

        def add_qa(index: int, items: List[bs4.PageElement]):
            q: str = items[0].get_text().replace(' ', '').strip()
            if '、' in q:
                q = q[q.index('、') + 1:]
            a = '\n'.join(map(lambda x: x.get_text(), items[1:])).replace(' ', '').replace('答：', '').strip()
            if len(q) == 0 or len(a) == 0:
                return
            qa.append(QaItem(
                question=q,
                answer=a,
                other={
                    "classification": classification_name
                }
            ))

        for i in range(len(question_box_index_list)):
            if i == len(question_box_index_list) - 1:
                add_qa(i + 1, children[question_box_index_list[i]:])
            else:
                add_qa(i + 1, children[question_box_index_list[i]:question_box_index_list[i + 1]])

        return qa
