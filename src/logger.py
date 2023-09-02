import logging
import inspect
from logging import handlers


def get_logger() -> logging.Logger:
    return logging.getLogger('Organizer')


def setup_logger() -> None:
    # Create formater
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # Create console handler and add formatter to it
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # Create console handler and add formatter to it
    fh = handlers.RotatingFileHandler(
        filename='log.log',
        maxBytes=5*1024*1024,
        backupCount=2,
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Get and update logger object
    log = get_logger()
    log.addHandler(ch)
    log.addHandler(fh)

    # Set default level as DEBUg - stream handlers will control flows
    log.setLevel(logging.DEBUG)


def log(level, msg: str):
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    full_msg = "(%s:%d) - %s" % (caller.filename, caller.lineno, msg)
    get_logger().log(level=level, msg=full_msg)


def debug(msg: str) -> None:
    log(level=logging.DEBUG, msg=msg)


def info(msg: str) -> None:
    log(level=logging.INFO, msg=msg)


def warning(msg: str) -> None:
    log(level=logging.WARNING, msg=msg)


def error(msg: str) -> None:
    log(level=logging.ERROR, msg=msg)


def critical(msg: str) -> None:
    log(level=logging.CRITICAL, msg=msg)


def main():
    setup_logger()


main()
