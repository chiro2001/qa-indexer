import spiders
from spiders import *
from spiders import Dummy


def main():
    tested_spiders = []
    testing_spiders = [
        Dummy
    ]
    spiders.run(tested_spiders)
    spiders.run(testing_spiders)
    logger.info("Done")


if __name__ == '__main__':
    main()
