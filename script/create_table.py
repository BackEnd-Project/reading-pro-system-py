import storage.model as model

try:
    # 数据库连接
    database = model.database

    # 模型
    user = model.User
    userAccount = model.UserAccount
    userSetting = model.UserSetting
    userSubscriber = model.UserSubscriber
    accountType = model.AccountType
    userPlatform = model.UserPlatform
    broker = model.Broker

    # 创建数据表，safe=True表示数据表不存在才去创建
    database.create_tables([user, userAccount, userSetting, userSubscriber, accountType, userPlatform, broker], safe=True)
    # 关闭数据库连接
    database.close()
except Exception as e:
    print("创建表时发生错误")

print("创建表成功")
