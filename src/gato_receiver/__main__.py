from gato_receiver.logger import setup_logger
from gato_receiver import app

import argparse


desc_str = """Radio service based on a HackRF One."""

parser = argparse.ArgumentParser(description=desc_str)
parser.add_argument(
    "-d", "--debug",
    action="store_true",
    help="Run in debug mode.",
)
parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Disable logging.",
)
parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Run in verbose mode.",
)

args = parser.parse_args()

setup_logger()
main_app = app.App()
main_app.run()
