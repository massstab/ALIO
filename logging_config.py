import logging


def configure_logging(logginglevel="INFO", log_to_console=True):
    if logginglevel == "DEBUG":
        level = logging.DEBUG
    elif logginglevel == "INFO":
        level = logging.INFO
    elif logginglevel == "WARNING":
        level = logging.WARNING
    elif logginglevel == "ERROR":
        level = logging.ERROR
    elif logginglevel == "CRITICAL":
        level = logging.CRITICAL
    else:
        level = logging.NOTSET

    logging.basicConfig(filename='interaction.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=level)

    # Create a StreamHandler to output the log messages to the console
    console_handler = logging.StreamHandler()

    # Add the StreamHandler to the root logger
    if log_to_console:
        logging.getLogger().addHandler(console_handler)
