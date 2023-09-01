import logging
import inspect


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
    fh = logging.FileHandler(filename='log.log')
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


def main():
    setup_logger()


main()
