#!/usr/bin/env python3
'''Defines a filtered_logger module with functions'''
import re


def filter_datum(fields: list, redaction: str,
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
