from spiders import *
from spiders.dfzq import Dfzq
from spiders.utils.run import run


def main():
    tested_spiders = [
        Dummy
    ]
    testing_spiders = [
        Dfzq
    ]
    # run(tested_spiders)
    run(testing_spiders)
    logger.info("Done")


if __name__ == '__main__':
    main()
