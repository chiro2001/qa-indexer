from typing import *
from spiders.utils.beans import QaItem
from spiders.dummy.parser import parser


def fetcher(page: int) -> List[QaItem]:
    return parser("")
