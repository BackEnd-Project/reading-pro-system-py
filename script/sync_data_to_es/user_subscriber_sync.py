import storage.model as model
import storage.es as es
import peewee

user_subscribers = model.UserSubscriber.select()
es_user_subscriber = es.UserSubscriber()

for user_subscriber in user_subscribers:
    try:
        es_user_subscriber.save(user_subscriber)
    except Exception as e:
        print(str(e))
        user_subscriber_id = user_subscriber.id
        print(user_subscriber_id + ":" + "同步到es失败")

# 删除es中多余的数据（在数据库不存在，但是在es中有）
es_user_subscribers = es_user_subscriber.get_all()
for user_subscriber in es_user_subscribers:
    try:
        model.UserSubscriber.get(model.UserSubscriber.id == user_subscriber.get("id"))
    except peewee.DoesNotExist:
        es_user_subscriber.delete(user_subscriber.get("id"))

print("同步完成")