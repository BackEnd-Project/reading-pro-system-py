"""
social_broker 表的手机号、邮箱加脚本
"""

import storage.model as model
from common import password_utils

brokers = model.Broker.select()
aes = password_utils.AESCipher()
for broker in brokers:
    try:
        raw_uemail = broker.uemail
        raw_uphone = broker.uphone

        broker.uemail = aes.encrypt(raw_uemail)
        broker.hash_uemail = password_utils.hash_md5(raw_uemail)

        broker.uphone = aes.encrypt(raw_uphone)
        broker.hash_uphone = password_utils.hash_md5(raw_uphone)

        broker.save()
    except Exception:
        pass

model.database.close()
print("更新成功")