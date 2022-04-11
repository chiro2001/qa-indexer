from spiders.base import *


class PingAnStatic(StaticSpider):
    NAME = "中国平安-科创板相关问题与解答"

    def __init__(self):
        super().__init__(PingAnStatic.NAME, "text/科创板相关问题与解答.txt")

    def parse_html(self, html: str) -> List[QaItem]:
        qa: List[QaItem] = []
        lines: List[AnyStr] = html.split('\n')
        lines = [line.strip() for line in lines if len(line) > 0]
        question_index_list: List[int] = []
        for i in range(len(lines)):
            if lines[i].startswith('问：'):
                question_index_list.append(i)

        def add_qa(items: List[AnyStr]):
            q = items[0][2:]
            a = '\n'.join(map(lambda x: x.replace('答：', ''), items[1:]))
            qa.append(QaItem(
                question=q,
                answer=a,
                other={
                    "classification": "科创板相关问题与解答"
                }
            ))

        for i in range(len(question_index_list)):
            if i == len(question_index_list) - 1:
                add_qa(lines[question_index_list[i]:])
            else:
                add_qa(lines[question_index_list[i]:question_index_list[i + 1]])
        return qa
