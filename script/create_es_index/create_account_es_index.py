import common
import config

index = common.get_index_social_user_unique(config.elastic_type_social_user_account)
es = common.get_es_social()

# 初始化索引的Mappings设置
_index_mappings ={
    "mappings": {
        "user_account": {
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "uuid": {
                    "type": "keyword"
                },
                "appid": {
                    "type": "keyword"
                },
                "account": {
                    "type": "keyword"
                },
                "investor_password": {
                    "type": "text"
                },
                "account_name": {
                    "type": "keyword"
                },
                "account_type": {
                    "type": "text"
                },
                "binding_type": {
                    "type": "text"
                },
                "account_abstract": {
                    "type": "text"
                },
                "update_switch": {
                    "type": "integer"
                },
                "update_status": {
                    "type": "text"
                },
                "account_display": {
                    "type": "integer"
                },
                "platform_display": {
                    "type": "integer"
                },
                "finance_display": {
                    "type": "integer"
                },
                "history_scope": {
                    "type": "text"
                },
                "position_scope": {
                    "type": "text"
                },
                "is_deleted": {
                    "type": "integer"
                },
                "update_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "create_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            }
        }
    }
}

if es.indices.exists(index=index) is True:
    es.indices.delete(index=index)

res = es.indices.create(index=index, body=_index_mappings)
print('创建es成功')