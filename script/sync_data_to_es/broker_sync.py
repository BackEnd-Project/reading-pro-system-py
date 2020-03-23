import storage.model as model
import storage.es as es
import peewee

brokers = model.Broker.select()
es_broker = es.Broker()

for broker in brokers:
    try:
        es_broker.save(broker)
    except Exception as e:
        print(str(e))
        uuid = broker.uuid
        print(uuid + ":" + "同步到es失败")

# 删除es中多余的数据（在数据库不存在，但是在es中有）
es_brokers = es_broker.get_all()
for broker in es_brokers:
    try:
        model.Broker.get(model.Broker.uuid == broker.get("uuid"))
    except peewee.DoesNotExist:
        es_broker.delete(broker.get("uuid"))

print("同步完成")