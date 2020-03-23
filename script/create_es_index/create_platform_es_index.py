import common
import config

index = common.get_index_social_user_unique(config.elastic_type_social_platform)
es = common.get_es_social()

# 初始化索引的Mappings设置
_index_mappings ={
    "mappings": {
        "user_platform": {
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
                "source_appid": {
                    "type": "keyword"
                },
                "source_uuid": {
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