import argparse
import logging
from config import Config # type: ignore


def setup_logger(config: Config) -> None:
    logger = logging.getLogger(config.get("logging", "LoggerName"))
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(config.get("logging", "LoggerFormat"))
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(int(config.get("logging", "LoggerLevel")))
    logger.addHandler(stream_handler)


def main() -> None:
    config = Config()
    config.load()  # type: ignore
    config.get("logging", "LoggerName")
    from parser.isdn import ISDNParser, ISDNOutput  # type: ignore
    parser = argparse.ArgumentParser(description='This module is used to parse isdn messages')
    parser.add_argument('-f', '--file', help='import a text file', type=str)
    parser.add_argument('-s', '--search', action='store_const', const='True', help='Enable the search flag')
    parser.add_argument('-cgn', '--calling', help='Calling Number', type=str)
    parser.add_argument('-cdn', '--called', help='Called Number', type=str)
    parser.add_argument('-ca', '--cause', help='Cause Code', type=str)
    args = parser.parse_args()
    isdn_parser = ISDNParser(text_file=args.file)
    calls = ISDNOutput(isdn_calls=isdn_parser.parse_calls())
    calls.print_calls(search=args.search,
                      calling_number=args.calling,
                      called_number=args.called,
                      cause=args.cause)


if __name__ == "__main__":
    main()
