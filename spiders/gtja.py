from spiders.base import *


class GtjaCommonProblem(StaticSpider):
    NAME = "国泰君安"

    def __init__(self):
        super().__init__(GtjaCommonProblem.NAME, "常见问题-国泰君安证券福建站官网.html")

    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
        qa: List[QaItem] = []
        soup = Soup(html, "html.parser")
        qa_box = soup.select_one('ul[class="proplem-qa"]')
        classifications = qa_box.select('dl')

        for classification in classifications:
            classification_name = classification.select_one('dt').get_text().strip()
            classification_name = classification_name[classification_name.index('.') + 1:]
            logger.info(classification_name)

            lines = classification.select_one('dd').get_text().strip().split('\n')
            lines = [line.strip().replace("问：", "").replace("答：", "") for line in lines if len(line) > 0]
            logger.info(f'{len(lines)} lines')

            split_formats = ["%d", "Q%d"]
            strips = ["：", ' ', '、', '.']
            split_format = None
            strip = None
            for fmt in split_formats:
                split_symbol_now = fmt % 1
                found_fmt = False
                for s in strips:
                    if lines[0].startswith(f"{split_symbol_now}{s}") or lines[1].startswith(f"{split_symbol_now}{s}"):
                        found_fmt = True
                        split_format = fmt
                        strip = s
                        break
                if found_fmt:
                    break
            logger.info(f"{split_format} - {strip}")

            def get_starter(index_target: int) -> str:
                return f"{split_format}{strip}" % index_target

            def get_line_index(index_target: int) -> int:
                for j in range(len(lines)):
                    if lines[j].startswith(get_starter(index_target)):
                        return j
                return -1

            def add_qa(index_target: int, line_slice: List[str]):
                q = line_slice[0].replace(get_starter(index_target), "").strip()
                a = '\n'.join(line_slice[1:])
                logger.info(f"i = {index_target}, {q}")
                qa.append(QaItem(
                    question=q,
                    answer=a,
                    other={
                        "classification": classification_name
                    }
                ))

            last_index = -1
            for i in range(1, 1000):
                index = get_line_index(i)
                if index < 0:
                    if last_index < 0:
                        continue
                    else:
                        # print(lines[last_index:])
                        add_qa(i - 1, lines[last_index:])
                        break
                # logger.warning(lines[index])
                if last_index >= 0:
                    # print(lines[last_index:index])
                    add_qa(i - 1, lines[last_index:index])
                last_index = index
        return qa
