from validator import validate, Required
import error
import re


def setting_create(input_dict):
    rules = {
        "appid": [Required, lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "open_share": [lambda x: (isinstance(x, int) or (isinstance(x, str)))],
        "open_auto_audit": [lambda x: (isinstance(x, int) or (isinstance(x, str)))],
        "order_break_point": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "p_profit_share_ratio": [lambda x: (isinstance(x, float) or (isinstance(x, int)))],
        "f_profit_share_ratio": [lambda x: (isinstance(x, float) or (isinstance(x, int)))],
        "billing_period": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "billing_week": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "billing_date": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "account_setting": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "type": [Required, lambda x: (isinstance(x, str) and re.match("\w+", x))]
    }
    errors = {
        "appid": "appid is not existed or invalid",
        "open_share": "open_share is invalid",
        "open_auto_audit": "open_auto_audit is invalid",
        "order_break_point": "order_break_point is invalid",
        "p_profit_share_ratio": "p_profit_share_ratio is invalid",
        "f_profit_share_ratio": "f_profit_share_ratio is invalid",
        "billing_period": "billing_period is invalid",
        "billing_week": "billing_week is invalid",
        "billing_date": "billing_date is invalid",
        "account_setting": "account_setting is invalid",
        "type": "type is not existed or invalid"
    }
    default_error = "Params Invalid!"
    res = validate(rules, input_dict)
    if res.valid is False:
        # 抛出第一个参数验证的错误
        for key in res.errors:
            raise error.RequestData(error.request_data_error, errors.get(key, default_error))


def setting_delete(input_dict):
    rules = {
        "id": [Required, lambda x: (isinstance(x, str) and x != '')],
    }
    errors = {
        "id": "id is not existed or invalid",
    }
    default_error = "Params Invalid!"
    res = validate(rules, input_dict)
    if res.valid is False:
        # 抛出第一个参数验证的错误
        for key in res.errors:
            raise error.RequestData(error.request_data_error, errors.get(key, default_error))


def setting_update(input_dict):
    rules = {
        "id": [Required, lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "open_share": [lambda x: (isinstance(x, int) or (isinstance(x, str)))],
        "open_auto_audit": [lambda x: (isinstance(x, int) or (isinstance(x, str)))],
        "order_break_point": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "p_profit_share_ratio": [lambda x: (isinstance(x, float) or (isinstance(x, int)))],
        "f_profit_share_ratio": [lambda x: (isinstance(x, float) or (isinstance(x, int)))],
        "billing_period": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "billing_week": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "billing_date": [lambda x: (isinstance(x, str) and re.match("\w+", x))],
        "account_setting": [lambda x: (isinstance(x, str) and re.match("\w+", x))]
    }
    errors = {
        "id": "id is not existed or invalid",
        "open_share": "open_share is invalid",
        "open_auto_audit": "open_auto_audit is invalid",
        "order_break_point": "order_break_point is invalid",
        "p_profit_share_ratio": "p_profit_share_ratio is invalid",
        "f_profit_share_ratio": "f_profit_share_ratio is invalid",
        "billing_period": "billing_period is invalid",
        "billing_week": "billing_week is invalid",
        "billing_date": "billing_date is invalid",
        "account_setting": "account_setting is invalid"
    }
    default_error = "Params Invalid!"
    res = validate(rules, input_dict)
    if res.valid is False:
        # 抛出第一个参数验证的错误
        for key in res.errors:
            raise error.RequestData(error.request_data_error, errors.get(key, default_error))


def setting_get(input_dict):
    rules = {
        "id": [lambda x: (isinstance(x, str))],
        "page": [lambda x: (isinstance(x, int) or re.match("\d+", x)) or isinstance(x, int)],
        "pagesize": [lambda x: (isinstance(x, int) or re.match("\d+", x)) or isinstance(x, int)],
    }
    errors = {
        "id": "id is not existed or invalid",
        "page": "page is invalid int",
        "pagesize": "pagesize is invalid int"
    }
    default_error = "Params Invalid!"
    res = validate(rules, input_dict)
    if res.valid is False:
        # 抛出第一个参数验证的错误
        for key in res.errors:
            raise error.RequestData(error.request_data_error, errors.get(key, default_error))


