import common
from config import data_not_deleted

class Base:

    es = None

    def __init__(self):
        self.es = common.get_es_social()

    @staticmethod
    def get_total_counts(es_query_result):
        """
        根据es的查询结果，获取符合条件的总条数，主要用于分页的总页数
        :param es_query_result:
        :return:
        """
        return es_query_result.get("hits", {}).get("total", 0)

    @staticmethod
    def add_not_deleted_to_query(query):
        """
        为es查询语添加is_deleted = 0条件
        :param query:
        :return:
        """
        not_delete = {"term": {"is_deleted": data_not_deleted}}
        if query.get("query", {}).get("bool", {}).get("must") is not None:
            query["query"]["bool"]["must"].append(not_delete)
        elif query.get("query") is not None and query.get("query", {}).get("bool") is None:
            query["query"]["bool"] = {}
            query["query"]["bool"]["must"] = [not_delete]
        else:
            query["query"] = {}
            query["query"]["bool"] = {}
            query["query"]["bool"]["must"] = [not_delete]
        return query

    def beautify_search_result(self, es_result):
        """
        整理查询结果
        :param es_query_result:
        :return:
        """
        data = []
        try:
            hits = es_result.get("hits").get("hits")
            for hit in hits:
                data.append(hit.get('_source'))
            return data
        except Exception:
            return data



