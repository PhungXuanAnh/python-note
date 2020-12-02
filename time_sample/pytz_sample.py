import pytz
import datetime

def print_timezone():
    for tz in pytz.all_timezones:
        print(tz)

def find_time_now_base_timezone(timezone):
    tz = pytz.timezone(timezone)
    time_now_base_timezone = datetime.datetime.now(tz=tz)
    print(time_now_base_timezone.isoformat())

def show_datetime_object_base_timezone(timezone):
    # This timestamp is in UTC
    my_ct = datetime.datetime.now(tz=pytz.UTC)

    # Now convert it to another timezone
    tz = pytz.timezone(timezone)
    new_ct = my_ct.astimezone(tz=tz)
    print("UTC: {} --> {}".format(my_ct, new_ct.isoformat()))


if __name__ == '__main__':
    # Reference: https://www.unixtimestamp.com/
    
    # print_timezone()

    # find_time_now_base_timezone("Africa/Lusaka")
    # find_time_now_base_timezone("Asia/Saigon")
    # find_time_now_base_timezone("America/Miquelon")

    show_datetime_object_base_timezone("Africa/Lusaka")
    show_datetime_object_base_timezone("Asia/Saigon")
    show_datetime_object_base_timezone("America/Miquelon")
    