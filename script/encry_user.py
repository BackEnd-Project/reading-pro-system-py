# 邮箱、手机号加密脚本

import storage.model as model
from common import password_utils

users = model.User.select()
aes = password_utils.AESCipher()
for user in users:


    email1 = aes.decrypt(user.uemail)
    raw_uemail = aes.decrypt(email1)

    uphone1 = aes.decrypt(user.uphone)
    raw_uphone = aes.decrypt(uphone1)


    user.uemail = aes.encrypt(raw_uemail)
    user.hash_uemail = password_utils.hash_md5(raw_uemail)

    user.uphone = aes.encrypt(raw_uphone)
    user.hash_uphone = password_utils.hash_md5(raw_uphone)

    user.save()

model.database.close()

print("更新成功")
