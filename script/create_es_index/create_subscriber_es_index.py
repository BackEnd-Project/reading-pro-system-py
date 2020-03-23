import common
import config

index = common.get_index_social_user_unique(config.elastic_type_social_user_subscriber)
es = common.get_es_social()

# 初始化索引的Mappings设置
_index_mappings ={
    "mappings": {
        "user_subscriber": {
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
                "server_id": {
                    "type": "keyword"
                },
                "sub_id": {
                    "type": "keyword"
                },
                "sub_account": {
                    "type": "keyword"
                },
                "sub_uuid": {
                    "type": "keyword"
                },
                "sub_appid": {
                    "type": "keyword"
                },
                "sub_server_id": {
                    "type": "keyword"
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