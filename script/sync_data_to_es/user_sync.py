import storage.model as model
import storage.es as es
import common
import config
import peewee
import sys
from tornado.options import define

app_path = sys.path[0] + "/../.."
define("app_path", default=app_path)

es_user = es.User()

user_platforms = model.UserPlatform.select()

for user_platform in user_platforms:
    try:
        user = model.User.get(model.User.uuid == user_platform.uuid)
        es_user.save(user_platform.appid, user)
    except Exception as e:
        print(str(e))
        uuid = user_platform.uuid
        print(uuid + ":" + "同步到分es失败")

# 这个理论上不能这么弄，正常的用户应该都在platform中
users = model.User.select()
for user in users:
    try:
        es_user.save_to_general_index(user)
    except Exception as e:
        print(user.uuid + ":" + "同步到总的es失败")

# # 删除es中多余的数据（在数据库不存在，但是在es中有）
# index = common.get_index_social_user("*", config.elastic_type_social_user),
# query = {
#     "size": 10000
# }
# es_users, count = es_user.index_dsl_get(index, query)
# for user in es_users:
#     try:
#         model.UserPlatform.get(model.UserPlatform.uuid == user.get("uuid"))
#     except peewee.DoesNotExist:
#         es_user.delete(user.get("uuid"))

print("同步完成")