from spiders import *
from spiders.dfzq import Dfzq
from spiders.shzq import ShzqIPO, ShzqInvestors
from spiders.utils.run import run


def main():
    tested_spiders = [
        Dummy,
        # 东方证券
        Dfzq,
        # 上海证券 - IPO问题
        ShzqIPO,
    ]
    testing_spiders = [
        # ShzqIPO,
        ShzqInvestors,
    ]
    # run(tested_spiders)
    run(testing_spiders)
    logger.info("Done")


if __name__ == '__main__':
    main()
