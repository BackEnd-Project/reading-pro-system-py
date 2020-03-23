import storage.model as model
import storage.es as es
import peewee

user_platforms = model.UserPlatform.select()
es_user_platform = es.UserPlatform()

for user_platform in user_platforms:
    try:
        es_user_platform.save(user_platform)
    except Exception as e:
        print(str(e))
        user_platform_id = user_platform.id
        print(user_platform_id + ":" + "同步到es失败")

# 删除es中多余的数据（在数据库不存在，但是在es中有）
es_user_platforms = es_user_platform.get_all()
for user_platform in es_user_platforms:
    try:
        model.UserPlatform.get(model.UserPlatform.id == user_platform.get("id"))
    except peewee.DoesNotExist:
        es_user_platform.delete(user_platform.get("id"))

print("同步完成")