from common import password_utils
import storage.model as model

aes = password_utils.AESCipher()
user_accounts = model.UserAccount.select()


for user_account in user_accounts:
    try:
        user_account.investor_password = aes.encrypt(user_account.investor_password)
        user_account.save()
    except Exception as e:
        print(str(e))
        user_account_id = user_account.id


