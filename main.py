from spiders import *
from spiders.dfzq import Dfzq
from spiders.gtja import GtjaCommonProblem
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
    ]
    testing_spiders = [
        GtjaCommonProblem
    ]
    # run(tested_spiders)
    run(testing_spiders)
    logger.info("Done")


if __name__ == '__main__':
    main()
