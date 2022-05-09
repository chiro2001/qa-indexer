from spiders.base import *


class Shdfzq(StaticSpider):
    NAME = "上海东方证券资产"

    def __init__(self):
        super().__init__(Shdfzq.NAME, "上海东方证券资产.html")

    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
        soup = Soup(html, "html.parser")
        qa: List[QaItem] = []
        style_marks = [
            # 查找到上一层的 <p/>
            "color: rgb(192, 80, 77);",
            # 在本层划定范围即可
            "font-family: 微软雅黑, 'Microsoft YaHei'; color: rgb(255, 0, 0);",
            # 在本层划定范围即可
            "COLOR: #cc0000"
        ]

        def get_flatten_list(item):
            p = item.parent
            while p is None or (p is not None and p.name != 'p'):
                p = p.parent
            return p

        def parse_one_classification(index: int):
            part = soup.select_one(f"#data-{index}")
            classification = part.attrs['class'][0].split('-')
            print(classification)
            selected_mark = None
            selected_style = None
            for style in style_marks:
                selected_mark = part.find(attrs={"style": style})
                if selected_mark is not None:
                    selected_style = style
                    break
            if selected_mark is None:
                msg = f"cannot find selected mark in #data-{index}"
                logger.error(msg)
                raise LookupError(msg)
            selected_mark_all = [get_flatten_list(m) for m in
                                 part.find_all(attrs={"style": selected_style})]
            print(len(selected_mark_all), selected_mark_all[0])
            parent = selected_mark_all[0].parent
            children = list(parent.children)

            children_index = [children.index(m) for m in selected_mark_all]
            children_slice = []
            for i in range(len(children_index) - 1):
                children_slice.append([item for item in children[children_index[i]: children_index[i + 1]]
                                       # if not isinstance(item, NavigableString)
                                       ])
            children_slice = [c for c in children_slice if len(c) > 0]
            children_slice.append(children[children_index[-1]:])

            def parse_children_slice(s) -> Optional[QaItem]:
                q = s[0].get_text().replace(' ', '').replace('Q：', '')
                if '、' in q:
                    q = q.split('、')[-1]
                content = Soup("")
                [content.append(item) for item in s[1:]]
                if len(content) > 20:
                    # err... f**king docs
                    return None
                print(f"len content: {len(content)}")
                a = str(content).strip().replace(' ', '').replace('A：', '')
                print(f"q: {q}")
                print(f"a: {a}")
                if len(q) == 0 or len(a) == 0:
                    return None
                return QaItem(
                    question=q,
                    answer=a,
                    other={
                        'classification': classification[-1],
                        "rough": classification[0]
                    }
                )

            # print(children_slice[0])
            parsed_qa_list = [parse_children_slice(s) for s in children_slice]
            [qa.append(p) for p in parsed_qa_list if p is not None]

        [parse_one_classification(i) for i in range(1, 11)]
        return qa
