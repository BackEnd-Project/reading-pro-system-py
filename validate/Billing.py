from validator import validate, Required
import error
import re

def billing_get(input_dict):
    rules = {
        "serial": [lambda x: (isinstance(x, str))],
        "page": [lambda x: (isinstance(x, int) or re.match("\d+", x)) or isinstance(x, int)],
        "pagesize": [lambda x: (isinstance(x, int) or re.match("\d+", x)) or isinstance(x, int)],
    }
    errors = {
        "serial": "serial is not existed or invalid",
        "page": "page is invalid int",
        "pagesize": "pagesize is invalid int"
    }
    default_error = "Params Invalid!"
    res = validate(rules, input_dict)
    if res.valid is False:
        # 抛出第一个参数验证的错误
        for key in res.errors:
            raise error.RequestData(error.request_data_error, errors.get(key, default_error))

def billing_audit_create(input_dict):
    rules = {
        "id": [Required, lambda x: (isinstance(x, str))],
        "audit_type": [Required, lambda x: (isinstance(x, int) or re.match("\d+", x)) or isinstance(x, int)],
        "audit_comment": [lambda x: (isinstance(x, str))],
        "audit_uuid": [Required, lambda x: (isinstance(x, str))],
    }
    errors = {
        "id": "id is not existed or invalid",
        "audit_type": "audit_type is invalid",
        "audit_comment": "audit_comment is invalid",
        "audit_uuid": "audit_uuid is not existed or invalid"
    }
    default_error = "Params Invalid!"
    res = validate(rules, input_dict)
    if res.valid is False:
        # 抛出第一个参数验证的错误
        for key in res.errors:
            raise error.RequestData(error.request_data_error, errors.get(key, default_error))