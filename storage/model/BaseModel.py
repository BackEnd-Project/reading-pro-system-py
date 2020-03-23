from peewee import *
from .DbConnection import database

# 测试环境数据库
# database = MySQLDatabase('social_user', **{'host': '119.147.37.56', 'password': 'abc123', 'port': 13308, 'user': 'root', 'charset': 'utf8'})


class BaseModel(Model):
    class Meta:
        database = database

