import time

from spiders.base import *


class PingAnStatic(StaticSpider):
    NAME = "中国平安-科创板相关问题与解答"

    def __init__(self):
        super().__init__(PingAnStatic.NAME, "text/科创板相关问题与解答.txt")

    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
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


class PingAn(WebSpider):
    NAME = "中国平安"

    class URL:
        GET_CATEGORY = "https://stock.pingan.com/news/v1/help/api/enableCategory"
        GET_CATEGORY_DETAILS = "https://stock.pingan.com/news/v1/help/api/parent/list"
        GET_QUESTION_LIST = "https://stock.pingan.com/news/v1/help/api/children/list"
        GET_QUESTION_DETAILS = "https://stock.pingan.com/news/v1/help/api/detail"

    def __init__(self):
        self.category: List[Dict] = []
        self.category_details: Dict[str, List[Dict]] = {}
        self.question_info_list: List[Dict] = []
        super().__init__(self.NAME)

    def get_cookie(self) -> str:
        return "SD_RV=1.0; SD_UID=bebe0fce2aac44d281a43962dcb2e659; " \
               "WEBTRENDS_ID=eb883b57-d470-0649-e556-c4ac5561fe28; " \
               "BIGipServersis-stock-frontend-pc-static_30074_PrdPool=1209012652.31349.0000; " \
               "BIGipServerPrdPool_ng-dsp-hbd-loglib_8010=1360007596.18975.0000; " \
               "BIGipServerPrdPool_ng-dsp-ccs-info_8060=1343230380.31775.0000; " \
               "SD_SID=8874dffea31244f4837d268c561d9197; " \
               "WT-FPC=id=2a8aa5867cc3a1fd3501648562839790:lv=1649670403465:ss=1649670192142:" \
               "fs=1648562839790:pn=9:vn=2; SD_SET=1649674207059"

    @staticmethod
    def get_request_wrapper(
            asc: int = 0,
            ps: int = 20000,
            pn: int = 0,
            **kwargs):
        request_wrapper = {
            "appName": "pa18",
            "cltplt": "web",
            "cltver": "2.1",
            "channel": "pa18",
            'body': {
                "asc": asc,
                "ps": ps,
                "pn": pn
            }
        }
        request_wrapper['body'].update(kwargs)
        return request_wrapper

    def fetch_page_count(self) -> int:

        # 先获取目录列表
        resp_category = self.request(
            self.URL.GET_CATEGORY,
            method='POST',
            headers={"Content-Type": "application/json;charset=UTF-8"},
            data=json.dumps(self.get_request_wrapper()))
        self.category = resp_category.json()['data']['result']
        # print(self.category)
        # 获取子目录
        for category in self.category:
            resp_category_details = self.request(
                self.URL.GET_CATEGORY_DETAILS,
                method='POST',
                headers={"Content-Type": "application/json;charset=UTF-8"},
                data=json.dumps(self.get_request_wrapper(categoryNameEn=category['categoryNameEn'])))
            # print(resp_category_details.json())
            details_list: List[Dict] = resp_category_details.json()['result']['childs']
            for details in details_list:
                details.update({'mainCategoryName': category['categoryName']})
            self.category_details[category['categoryName']] = details_list
        # 数一数子目录下每一个问题
        for category_name in self.category_details:
            category_info_list = self.category_details[category_name]
            for category_info in category_info_list:
                if 'details' in category_info:
                    for question_info in category_info['details']:
                        question_info_new: Dict = question_info.copy()
                        question_info_new.update({
                            'categoryName': category_info['categoryName'],
                            'mainCategoryName': category_info['mainCategoryName']
                        })
                        self.question_info_list.append(question_info_new)
        return len(self.question_info_list)

    def parse_content(self, html: str, **kwargs) -> List[QaItem]:
        # logger.warning(f"{kwargs}")
        content: Dict = json.loads(html)['result']
        q = content['description']
        a = content['content']
        a = Soup(a, 'html.parser')\
            .get_text()\
            .strip()\
            .replace('\t', '')\
            .replace(' ', '')\
            .replace('\n\n', '\n')\
            .replace('\n\n', '\n')\
            .replace('\n\n', '\n')\
            .replace('\n\n', '\n') if self.html_out else a
        # 什么自问自答
        if q == a:
            return []
        return [QaItem(
            question=q,
            answer=a,
            other={
                'classification': content['categorys'][0]['parentName'],
                'categoryName': content['categorys'][0]['categoryName']
            }
        ), ]

    def fetch_page_content(self, page: Optional[int] = None) -> str:
        target_question = self.question_info_list[page]
        target_id = target_question['id']

        def is_cached() -> bool:
            for response in self.session.cache.responses.values():
                if response.request.body == b'None':
                    continue
                req = json.loads(response.request.body)
                if 'body' not in req:
                    continue
                if 'id' not in req['body']:
                    continue
                if f"{target_id}" == req['body']['id']:
                    return True
            return False

        cached = is_cached()
        if not cached:
            time.sleep(0.5)
        resp = self.request(
            self.URL.GET_QUESTION_DETAILS,
            method='POST',
            headers={"Content-Type": "application/json;charset=UTF-8"},
            data=json.dumps(self.get_request_wrapper(id=f"{self.question_info_list[page]['id']}")))
        text = resp.text
        # print(text)
        return text
