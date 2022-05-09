from spiders import *
from spiders.dfzq import Dfzq
from spiders.fzzq import Fzzq
from spiders.gtja import GtjaCommonProblem
from spiders.pingan import PingAnStatic, PingAn
from spiders.shdfzq import Shdfzq
from spiders.shzq import ShzqIPO, ShzqInvestors
from spiders.utils.run import run


def main():
    tested_spiders = [
        Dummy,
        # 东方证券
        Dfzq,
        # 上海证券 - IPO问题
        ShzqIPO,
        # 上海证券 - 投资者问题
        ShzqInvestors,
        # 常见问题-国泰君安证券福建站
        GtjaCommonProblem,
        # 方正证券
        Fzzq,
        # 中国平安-科创板相关问题与解答
        PingAnStatic,
        # 中国平安（动态页面）
        PingAn
    ]
    testing_spiders = [
        # 上海东方证券资产
        Shdfzq
    ]
    # run(tested_spiders)
    run(testing_spiders)
    logger.info("Done")


if __name__ == '__main__':
    main()
