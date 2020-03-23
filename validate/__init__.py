# -*- coding: utf-8 -*-
"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
"""
from .PlatformSetting import *
from .Billing import *

__all__ = ['PlatformSetting', 'Billing']

reg_id = "(\w*_*)*"
reg_uuid = "(\w*_*)*"
reg_uphone = "\d*"
reg_uphonecode = "\d*"
reg_uemail = "^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
reg_uemails = ""
