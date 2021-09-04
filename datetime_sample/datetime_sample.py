"""
Created on Jun 26, 2017

@author: xuananh
"""
import datetime
import calendar
import pytz
import time
import dateutil.parser
from dateutil.tz import tzutc


def get_current_server_timezone_number():
    print(
        "\n------------------------ get_current_server_timezone_number ----------------------------------------"
    )
    print("timezone: ", time.tzname)


def list_all_timezones_string():
    print(
        "\n------------------------ list_all_timezones_string ----------------------------------------"
    )
    print("to list all timezone: ", "using this method: pytz.all_timezones")
    # print("all timezone: ", pytz.all_timezones)


def show_date_time_with_timezone():
    # reference: https://stackoverflow.com/a/25887393/7639845
    print(
        "\n------------------------show_date_time_with_timezone ----------------------------------------"
    )
    print("naive datetime with server timezone: ", datetime.datetime.now())
    print("naive datetime utc:                  ", datetime.datetime.utcnow())
    print("aware datetime utc:                  ", datetime.datetime.now(datetime.timezone.utc))
    print(
        "aware datetime with timezone = utc get from pytz:     ",
        datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.utc),
    )
    print(
        "aware datetime with timezone = utc get from datetime: ",
        datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone.utc),
    )
    print(
        "aware datetime with timezone = default:               ",
        datetime.datetime.now(datetime.timezone.utc).astimezone(),
    )
    print(
        "aware datetime with given  timezone = hcm:            ",
        datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone("Asia/Ho_Chi_Minh")),
    )
    print(
        "current datetime in given  timezone = hcm:            ",
        datetime.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
    )


def format_datetime_base_on_standard():
    print("\n----------------------------format_datetime_base_on_standard-------------------")
    print("UTC timestamp now 1: ", time.time())
    print("UTC timestamp now 2: ", datetime.datetime.now().timestamp())
    print("UTC timestamp now 3: ", datetime.datetime.utcnow())
    print("UTC timestamp now 4: ", calendar.timegm(time.gmtime()))
    print("UTC timestamp to datetime :       ", datetime.datetime.fromtimestamp(1575963196))
    print(
        "UTC timestamp to datatime - 24h : ",
        datetime.datetime.fromtimestamp(1575963196 - 24 * 60 * 60),
    )
    print("UTC timestamp to hour :       ", datetime.datetime.fromtimestamp(1575963196).hour)

    print("RFC 3339 format: ", dateutil.parser.parse("2008-09-03T20:56:35.450686Z"))
    print("                 ", datetime.datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc()))

    print("ISO 8601 extended format: ", dateutil.parser.parse("2008-09-03T20:56:35.450686"))
    print("                          ", datetime.datetime(2008, 9, 3, 20, 56, 35, 450686))

    print("ISO 8601 basic format: ", dateutil.parser.parse("20080903T205635.450686"))
    print("                       ", datetime.datetime(2008, 9, 3, 20, 56, 35, 450686))

    print("ISO 8601 basic format, date only: ", dateutil.parser.parse("20080903"))
    print("                                  ", datetime.datetime(2008, 9, 3, 0, 0))


def format_datetime_base_on_defined_string_format():
    print("\n-------------- format_datetime_base_on_defined_string_format -----------------------")
    my_time = dateutil.parser.parse("2018-06-06T08:01:53.420Z")
    print("my_time:          ", my_time)
    print("my_time formated: ", my_time.strftime("[%Y-%m-%d]-[%H:%M:%S]"))
    my_time = datetime.datetime.now()
    print("my_time:          ", my_time)
    print("my_time formated: ", my_time.strftime("[%Y-%m-%d]-[%H:%M:%S]"))


def parse_date_time_from_string():
    # see datetime format code here : https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    print("\n-------------- parse_date_time_from_string -----------------------")
    string_contain_date_time = 'Test string contain datetime Jun 1 2005  1:33PM'
    define_format_code_of_string_contain_date_time = 'Test string contain datetime %b %d %Y %I:%M%p'
    datetime_object = datetime.datetime.strptime(string_contain_date_time, define_format_code_of_string_contain_date_time)
    print(datetime_object)

    string_contain_date_time1 = 'Delivered Monday, August 16, 2021  at 10:37'
    define_format_code_of_string_contain_date_time1 = 'Delivered %A, %B %d, %Y at %H:%M'
    datetime_object = datetime.datetime.strptime(string_contain_date_time1, define_format_code_of_string_contain_date_time1)
    print(datetime_object)

def get_time_period():
    print(
        "\n----------------------------------get_time_period-----------------------------------------"
    )
    t1 = datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)
    t2 = datetime.datetime(2008, 9, 5, 20, 56, 45, 450686)
    duration = t2 - t1

    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return days, hours, minutes, seconds

    days, hours, minutes, seconds = convert_timedelta(duration)
    print("NOTE: It should use total_seconds when t2 - t1 > 1 day, see the difference below:")
    print("t2 - t1 = {} days".format(days))
    print("t2 - t1 = {} hours".format(hours))
    print("t2 - t1 = {} minutes".format(minutes))
    print("t2 - t1 = {} seconds".format(seconds))
    print("t2 - t1 = {} total_seconds".format(duration.total_seconds()))


def datetime_in_pass():
    print(
        "\n----------------------------------datetime_in_pass-----------------------------------------"
    )
    now = datetime.datetime.now()
    datetime_7_day_ago = now - datetime.timedelta(days=7)
    print("now :           ", now)
    print("date_7_day_ago: ", datetime_7_day_ago)

    today = datetime.date.today()
    date_7_day_ago = today - datetime.timedelta(days=7)
    print("today           ", today)
    print("date_7_day_ago: ", date_7_day_ago)


def date_time_in_future():
    print(
        "\n-------------------------------------date_time_in_future--------------------------------------"
    )
    now = datetime.datetime.now()
    datetime_7_day_ago = now + datetime.timedelta(days=7)
    print("now :                 ", now)
    print("date_7_day_in_future: ", datetime_7_day_ago)
    print("timestamp: ", datetime_7_day_ago.timestamp())

    today = datetime.date.today()
    date_7_day_ago = today + datetime.timedelta(days=7)
    print("today                 ", today)
    print("date_7_day_in_future: ", date_7_day_ago)
    print("timestamp: ", datetime_7_day_ago.timestamp())


def time_around_a_moment():
    print("\n--------------------------time_around_a_moment-------------------------------------")
    d = datetime.datetime.utcnow()
    for i in range(-2, 3):
        d1 = d + datetime.timedelta(minutes=i)
        print(d1.strftime("%Y-%m-%dT%H:%M"))
        # print(d1.strftime("%Y-%m-%d"))


def extract_year_month_day_hour_minute_second():
    print(
        "\n----------------------extract_year_month_day_hour_minute_second-----------------------"
    )
    print("year: ", datetime.datetime.now().year)
    print("month: ", datetime.datetime.now().month)
    print("day: ", datetime.datetime.now().day)
    print("hour: ", datetime.datetime.now().hour)
    print("minute: ", datetime.datetime.now().minute)
    print("second: ", datetime.datetime.now().second)


def convert_date_time__to__date_and_opposite():
    print("\n----------------------convert_date_time__to__date_and_opposite-----------------------")
    date_time = datetime.datetime.now()
    print("date_time to date: ", date_time.date())

    date = datetime.datetime.today()
    print("date to datetime:  ", datetime.datetime(date.year, date.month, date.day))


if __name__ == "__main__":
    print(datetime.date(1991, 1, 1))
    # get_current_server_timezone_number()
    # list_all_timezones_string()
    # show_date_time_with_timezone()

    # format_datetime_base_on_defined_string_format()
    parse_date_time_from_string()

    # get_time_period()

    # datetime_in_pass()
    # date_time_in_future()
    # time_around_a_moment()

    # extract_year_month_day_hour_minute_second()
    # convert_date_time__to__date_and_opposite()
