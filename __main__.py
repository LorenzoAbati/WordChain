
from WordChainApp.WordChainApp import WordChainApp
import logging

import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d|%(levelname)-8s|%(filename)s:%(lineno)d|%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def main():
    project_location = os.path.dirname(os.path.realpath(__file__))
    storage_location = project_location + "/Storage"

    app = WordChainApp(storage_location)


if __name__ == '__main__':
    main()
