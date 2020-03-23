import storage.model as model
import storage.es as es
import peewee
import sys
from tornado.options import define

app_path = sys.path[0] + "/../.."
define("app_path", default=app_path)

user_accounts = model.UserAccount.select()
es_user_account = es.UserAccount()

for user_account in user_accounts:
    try:
        es_user_account.save(user_account.appid, user_account)
    except Exception as e:
        print(str(e))
        user_account_id = user_account.id
        print(user_account_id + ":" + "同步到es失败")

# 删除es中多余的数据（在数据库不存在，但是在es中有）
es_user_accounts = es_user_account.get_all()
for user_account in es_user_accounts:
    try:
        model.UserAccount.get(model.UserAccount.id == user_account.get("id"))
    except peewee.DoesNotExist:
        es_user_account.delete(user_account.get("id"))


print("同步完成")