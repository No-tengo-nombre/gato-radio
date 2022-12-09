from gato_receiver import app
from gato_receiver.configs import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT
from gato_receiver.logger import setup_logger

import argparse


desc_str = """Radio service based on a HackRF One."""

parser = argparse.ArgumentParser(description=desc_str)
parser.add_argument(
    "-i", "--ip",
    action="store",
    type=str,
    help="Target ip.",
    default=DEFAULT_SERVER_IP,
)
parser.add_argument(
    "-p", "--port",
    action="store",
    type=int,
    help="Target port.",
    default=DEFAULT_SERVER_PORT,
)
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

setup_logger(args.quiet, args.debug, args.verbose)
main_app = app.App(args.ip, args.port)
main_app.run()
