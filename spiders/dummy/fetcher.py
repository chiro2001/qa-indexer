from typing import *
from spiders.utils.beans import QaItem
from spiders.dummy.parser import parser


def fetch_page_info() -> int:
    return 1


def fetcher(page: int) -> List[QaItem]:
    return parser("")
