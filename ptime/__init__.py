import calendar
import datetime
import time


def get_year():
    """
    获取当天日期的年份
    :return:
    """
    return datetime.datetime.now().year


def get_month():
    """
    获取当天日期的月份
    :return:
    """
    return datetime.datetime.now().month


def get_day():
    """
    获取当天日期的日
    :return:
    """
    return datetime.datetime.now().day


def get_date():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def next_date(date):
    """
    获取date的下一天，如2018-01-16，则返回2018-01-17
    :param date:
    :return:
    """
    date_unix = time.mktime(time.strptime(date, "%Y-%m-%d"))
    date_unix += 3600 * 24
    next_date_str = time.strftime("%Y-%m-%d", time.localtime(date_unix))
    return next_date_str


def get_yesterday():
    """
    获取昨天的日期
    :return: 类似2018-01-31
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def get_month_last_date(year, month):
    """
    获取一个月的最后一天的日期
    :param year:
    :param month:
    :return: 类似2018-01-31
    """
    return "{}-{}-{}".format(year, format_month(month), calendar.monthrange(int(year), int(month))[1])


def format_date(year, month, day):
    """
    根据年月日把日期组成2018-01-08这样的日期
    :param year: 2018
    :param month: 1
    :param day: 8
    :return: 2018-01-08
    """
    return "{}-{}-{}".format(year, format_month(month), format_day(day))


def get_month_first_date(year, month):
    """
    获取一个月的最开始的一天的日期
    :param year:
    :param month:
    :return: 类似2018-01-01
    """
    return "{}-{}-{}".format(year, format_month(month), "01")


def format_month(month):
    """
    把月份转化为两位数的格式，如6则变为06，12则还是12
    :param month:
    :return:
    """
    month = int(month)
    if month >= 10:
        return month
    else:
        return "{}{}".format(0, str(month))


def format_day(day):
    """
    把日转化为两位数的格式，如6则变为06，16则还是16
    :param day:
    :return:
    """
    day = int(day)
    if day >= 10:
        return day
    else:
        return "{}{}".format(0, str(day))


def format_date_for_es(date):
    """
    把2018-01-12的日期格式转变2018-01-12 00:00:00
    :param date:
    :return:
    """
    if date is None or date is "":
        return None
    date_unix = time.mktime(time.strptime(date, "%Y-%m-%d"))
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_unix))
    return date_str


def get_last_month_date(year, month):
    """
    获取上个月的这天的日期
    :param year:
    :param month:
    :return:
    """
    month = int(month)
    last_month = month - 1
    day = get_day()
    day = format_day(day)
    # 同一年
    if last_month >= 1:
        return "{}-{}-{}".format(year, last_month, day)
    # 不同一年
    else:
        last_year = year - 1
        return "{}-{}-{}".format(last_year, 12, day)


def get_last_3_month_date(year, month):
    """
    获取上3个月的今天
    :param year:
    :param month:
    :return:
    """
    month = int(month)
    last_3_month = month - 3
    day = get_day()
    day = format_day(day)
    # 同一年
    if last_3_month >= 1:
        return "{}-{}-{}".format(year, last_3_month, day)
    # 不同一年
    else:
        last_year = year - 1
        last_3_month = last_3_month + 12
        last_3_month = format_month(last_3_month)
        return "{}-{}-{}".format(last_year, last_3_month, day)


def get_last_6_month_date(year, month):
    """
    # 获取上6个月的今天
    """
    month = int(month)
    last_6_month = month - 6
    day = get_day()
    day = format_day(day)
    # 同一年
    if last_6_month >= 1:
        return "{}-{}-{}".format(year, format_month(last_6_month), day)
    # 不同一年
    else:
        last_year = year - 1
        last_6_month = last_6_month + 12
        last_6_month = format_month(last_6_month)
        return "{}-{}-{}".format(last_year, last_6_month, day)


def get_week_first_date():
    """
    #获取当前星期的第一天
    :return:
    """
    offset = datetime.datetime.now().weekday()
    today = datetime.date.today()
    offset_date = datetime.timedelta(days=offset)
    week_first_date = today - offset_date
    return week_first_date


def get_pre_week_first_date():
    """
    #获取上个星期的第一天
    :return:
    """
    offset = datetime.datetime.now().weekday() + 7
    today = datetime.date.today()
    offset_date = datetime.timedelta(days=offset)
    week_first_date = today - offset_date
    return week_first_date


def get_pre_week_current_date():
    """
    #获取上个星期的今天，如果今天是星期六，则返回上周的星期六的日期
    :return:
    """
    today = datetime.date.today()
    offset_date = datetime.timedelta(days=7)
    week_current_date = today - offset_date
    return week_current_date


def get_current_month_first_date():
    """
    获取当前月份的第一天
    :return:
    """
    today = datetime.date.today()
    return datetime.date(today.year, today.month, 1)


def get_current_month_last_date():
    """
    获取当前月份的最后一天
    :return:
    """
    today = datetime.date.today()
    return datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])


def get_pre_month_first_date():
    """
    获取上一个月的第一天
    :return:
    """
    pre_month_last_date = get_current_month_first_date() - datetime.timedelta(days=1)

    return datetime.date(pre_month_last_date.year, pre_month_last_date.month, 1)


def get_pre_month_last_date():
    """
    获取上一个月的最后一天
    :return:
    """
    pre_month_last_date = get_current_month_first_date() - datetime.timedelta(days=1)

    return pre_month_last_date


def get_pre_month_current_date():
    """
    获取上一个月的今天
    :return:
    """
    today = datetime.date.today()
    pre_month_last_date = get_current_month_first_date() - datetime.timedelta(days=1)
    return datetime.date(pre_month_last_date.year, pre_month_last_date.month, today.day)


def get_current_year_first_date():
    """
    获取今年的第一天
    :return:
    """
    today = datetime.date.today()
    return datetime.date(today.year, 1, 1)


def get_pre_year_first_date():
    """
    获取上一年的第一天
    :return:
    """
    pre_year_last_date = get_current_year_first_date() - datetime.timedelta(days=1)
    return datetime.date(pre_year_last_date.year, 1, 1)


def get_pre_2_year_first_date():
    """
    获取上2年的第一天（前年的第一天）
    :return:
    """
    year = datetime.date.today().year - 2
    return datetime.date(year, 1, 1)


def get_pre_date(offset):
    """
    offset前的日期
    :param
    :return:
    """
    today = datetime.date.today()
    return str(today - datetime.timedelta(days=offset))


if __name__ == "__main__":
    print(type(get_pre_date(1)))
    print(get_yesterday())
    print(get_current_year_first_date())
    print(datetime.datetime.now().month)
    print(datetime.date.today().weekday())
    print(datetime.datetime.now().weekday() + 7)
    print(datetime.datetime.now().weekday())
    print(get_week_first_date())
    print(type(datetime.datetime.now()))
    print(type(datetime.date.today()))

    from service.sStatistics import sStatistics
    s = sStatistics()
    print(s.__dict__)











