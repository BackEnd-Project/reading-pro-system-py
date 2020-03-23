import storage.model as model
import storage.es as es
import peewee

user_settings = model.UserSetting.select()
es_user_setting = es.UserSetting()

for user_setting in user_settings:
    try:
        es_user_setting.save(user_setting)
    except Exception as e:
        print(str(e))
        user_setting_id = user_setting.id
        print(user_setting_id + ":" + "同步到es失败")

# 删除es中多余的数据（在数据库不存在，但是在es中有）
es_user_settings = es_user_setting.get_all()
for user_setting in es_user_settings:
    try:
        model.UserSetting.get(model.UserSetting.id == user_setting.get("id"))
    except peewee.DoesNotExist:
        es_user_setting.delete(user_setting.get("id"))

print("同步完成")