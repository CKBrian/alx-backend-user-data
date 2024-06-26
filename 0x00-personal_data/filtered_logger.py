#!/usr/bin/env python3
'''Defines a filtered_logger module with functions '''
import re
from typing import List
import logging
import mysql.connector
import os


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
    logger.propagate = False
    # stream handler
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # adding output stream to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''returns a connector to the database
       (mysql.connector.connection.MySQLConnection object'''
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    usr = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connection.MySQLConnection(
                                                      host=host,
                                                      user=usr,
                                                      password=passwd,
                                                      database=db)
    return conn


def main() -> None:
    '''Entry point'''
    db = get_db()
    cursor = db.cursor()
    query = 'SELECT * FROM users;'
    cursor.execute(query)
    fields = [field[0] for field in cursor.description]
    logger = get_logger()
    for row in cursor:
        log_entry = '; '.join(f'{field}={val}'
                              for field, val in zip(fields, row))
        logger.info(log_entry)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
