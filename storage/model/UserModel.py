"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2018 DooHolding Inc. (http://www.doo.tech)
 *
 * May you do good and not evil
 * May you find forgiveness for yourself and forgive others
 * May you share freely, never taking more than you give.  -- SQLite source code
 *
 * As we enjoy great advantages from the inventions of others, we should be glad
 * of an opportunity to serve others by an invention of ours, and this we should
 * do freely and generously.  -- Ben Franklin
                     ..
               .`         `.:/:`      `-/+ooo
           `-/+oo/    `.:/ooooo-  `.:+ooooooo
       `.:+oooooo/ `-/+ooo++ooo- :oooo+/-+ooo
   `.:/oooo+/:ooo/ .ooo+:.`:ooo- /ooo-`  +ooo
  `:+ooooo.` `ooo/ .ooo:   :ooo- /ooo.   +ooo
    `.oooo   `ooo/ .ooo:   :ooo- /ooo.   +ooo
      +ooo   `ooo/ .ooo:   :ooo- /ooo.   +ooo
      +ooo   `ooo/ .ooo:   :ooo- /ooo.   +ooo
      +ooo   `ooo/ .ooo:   :ooo- /ooo. `.+ooo
      +ooo   .ooo/ .ooo:`.:+ooo- /ooo:/+oooo/
      +ooo-/+oooo: .ooo++ooo+/-` /oooooo+:-`
     `+oooooo+/-`  .ooooo/:.`    :oo+/-``   `
  `-/+oooo/-`      `://-`         `.`    `:/+
   .:/+:.`                                .:/
"""

from .BaseModel import *


class UserModel(BaseModel):
    uid = CharField(primary_key=True)  # 主键ID
    # appid = CharField()  # 经纪商ID
    password = CharField(null=True)  # 结算周
    email = CharField(null=True)  # 第几周
    name = CharField(null=True)  # 设置时的当前周（52周中的第几周）
    # billing_date = CharField(null=True)  # 结算日
    update_time = DateTimeField()  # 更新时间
    create_time = DateTimeField()  # 创建时间
    # account_setting = TextField()  # 体验账号设置
    # type = CharField()  # 类型
    is_deleted = IntegerField()  # 是否删除

    class Meta:
        table_name = 'rp_user'
