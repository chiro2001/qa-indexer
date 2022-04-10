from spiders import *
from spiders.dfzq import Dfzq
from spiders.shzq import Shzq
from spiders.utils.run import run


def main():
    tested_spiders = [
        Dummy,
        # 东方证券
        Dfzq
    ]
    testing_spiders = [
        Shzq
    ]
    # run(tested_spiders)
    run(testing_spiders)
    logger.info("Done")


if __name__ == '__main__':
    main()
