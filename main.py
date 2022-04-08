from spiders import *


def main():
    tested_spiders = []
    testing_spiders = [
        Dummy
    ]
    # spiders.run(tested_spiders)
    # spiders.run(testing_spiders)
    # run(testing_spiders)
    d = Dummy()
    d.run()
    logger.info("Done")


if __name__ == '__main__':
    main()
