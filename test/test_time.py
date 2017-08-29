import time
import datetime

from dateutil.parser import parse

print time.time()
print datetime.datetime.now()


print time.strftime('%Y-%m-%d %H:%M:%S')
print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print time.strptime('2017-02-28', '%Y-%m-%d')
# print time.strptime('2017-02-29', '%Y-%m-%d')

print datetime.datetime.strptime('2017-02-28', '%Y-%m-%d')
# print datetime.datetime.strptime('2017-02-29', '%Y-%m-%d')


def validate(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# def validate(date_text):
#     try:
#         parse(date_text)
#         return True
#     except ValueError:
#         return False

print validate('2017-02-28')
print validate('2017-02-29')
print validate('2017/02/28')


print time.strftime('%Y-%m-%d')


def validate(date_text):
    try:
        parse(date_text)
        return True
    except ValueError:
        return False
