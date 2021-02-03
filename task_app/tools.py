from datetime import datetime

from .const import DATE_FORMAT


class DateError(Exception):
    pass


def validate_date(date):
    if datetime.now().date() < date:
        raise DateError


def convert_date(date):
    date = date.split('.')
    date = '{}-{}-{}'.format(date[2], date[1], date[0])
    date = datetime.strptime(date, DATE_FORMAT).date()
    return date
