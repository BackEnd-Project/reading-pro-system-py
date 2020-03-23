import config
from playhouse.pool import PooledMySQLDatabase

# 使用连接池
# reading_pro_system
database = PooledMySQLDatabase(database=config.rp_db['db'], max_connections=300, **{
    'host': config.rp_db['host'],
    'port': int(config.rp_db['port']),
    'user': config.rp_db['user'],
    'passwd': config.rp_db['pass'],
    'charset': 'utf8'})


__all__ = ['database']
