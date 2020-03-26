
"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
 *
 * May you do good and not evil
 * May you find forgiveness for yourself and forgive others
 * May you share freely, never taking more than you give.  -- SQLite source code
 *
 * As we enjoy great advantages from the inventions of others, we should be glad
 * of an opportunity to serve others by an invention of ours, and this we should
 * do freely and generously.  -- Ben Franklin
 *
 *     (\
 *     (  \  /(o)\     caw!
 *     (   \/  ()/ /)
 *      (   `;.))'".)
 *       `(/////.-'
 *    =====))=))===()
 *      ///'
 *     //
 *    '
"""
import common
from storage.model.UserModel import UserModel as User
from storage.model.UserModel import database as database
from playhouse.shortcuts import model_to_dict
from peewee import fn
import logging
from common import password_utils


class sUser():

    def get_info(self, **kwargs):
        """
        获取用户详情
        :param kwargs
        :return object:
        """
        result = User.get_or_none((User.uid == kwargs['uid']) & (User.is_deleted == 0))
        database.close()
        if result is None:
            return {}
        else:
            result = model_to_dict(result)
            return result

    def create_user(self, **kwargs):
        """
        创建用户
        :param kwargs
        :return object:
        """
        try:
            database.connect(reuse_if_open=True)
            password = kwargs.get('password', None)
            if password:
                kwargs['password'] = password_utils.shal(password)
            kwargs['create_time'] = common.get_time_now()
            kwargs['update_time'] = common.get_time_now()
            kwargs['uid'] = common.generate_id()

            # 创建用户
            result = User.create(**kwargs)
            database.close()
            if result:
                return result
            else:
                return False
        except Exception as Err:
            logging.critical(Err)
            return False

    def get_list(self, **kwargs):
        """
        获取用户列表
        :param kwargs
        :return tuple:
        """
        page = kwargs.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
        pagesize = kwargs.get('pagesize')
        if pagesize is None:
            pagesize = 25
        else:
            pagesize = int(pagesize)
        condition = (User.is_deleted == 0)
        for key in kwargs.keys():
            condition = condition & (getattr(User, key) == kwargs[key])

        user_list = []
        if pagesize is None or pagesize == 0:
            # 判断是否需要分页返回数据
            for item in User.select().order_by(User.create_time.desc()).where(condition).dicts():
                user_list.append(item)
        else:
            # 判断是否需要分页返回数据
            for item in User.select().order_by(User.create_time.desc()).paginate(page, pagesize).where(condition).dicts():
                user_list.append(item)
        total_counts = User.select().where(condition).count()
        database.close()
        for items in user_list:
            if items['create_time'] is not None and items['create_time'] != '':
                items['create_time'] = common.datetime_to_string(items['create_time'])
            if items['update_time'] is not None and items['update_time'] != '':
                items['update_time'] = common.datetime_to_string(items['update_time'])
        # 返回数据列表
        return user_list, total_counts
