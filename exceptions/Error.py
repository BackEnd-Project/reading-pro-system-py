

exception = 20000 #使用python定义的错误信息
request_data_error = 20001 #请求参数验证出错

data_not_existed = 20002 #查找的数据不存在
data_save_error = 20003 #调用save方法时出错
data_delete_error = 20004 #数据库delete方法错误
data_error_not_know = 20005 #数据库那里发生未知错误
data_integrity_error = 20006 #数据库约束错误
es_save_error = 20007 #es保存出错
transaction_rollback = 20008 #事务回滚
data_already_exists = 20009 #数据已经存在

def get_error_message(code):
    reflect = {
        20001: "request params error",
        20002: "data you get not existed",
        20003: "database save error",
        20004: "database delete error",
        20005: "not know error",
        20006: "database constraint error",
        20007: "es save error",
        20008: "transaction rollback error",
        20009: "data already exists"
    }
    return reflect.get(code)