#!/usr/bin/env python3
'''Defines a filtered_logger module with functions '''
import re
from typing import List
import logging


PII_FIELDS = ("email", "phone", "ssn", "password", "name")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''
        returns the log message obfuscated

        Args:
            fields (list): list of strings repr all fields to obfuscate
            redaction (str): a string representing by what the field will be
                             obfuscated
            message (str): a string representing the log line
            separator (str): a string representing by which character is
                             separating all fields in the log line (message)
    '''
    for field in fields:
        message = re.sub(fr'{field}=[^{separator}]+',
                         f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filters values in incoming log records using filter_datum'''
        log_entry = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_entry, self.SEPARATOR)


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object.'''
    # logger and log levels
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    # stream handler
    formatter = RedactingFormatter([])
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # adding output stream to the logger
    logger.addHandler(stream_handler)

    return logger
