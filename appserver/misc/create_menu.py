#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2010-2013, Ryan Fan <ryan.fan@oracle.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Library General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""
from __future__ import absolute_import

from sdk.menu import MenuConfig, SubMenu, MenuItem, MENU_TYPE
from client import client

if __name__ == '__main__':
    menu_config = MenuConfig()
    menu1 = SubMenu(u'测试一')
    menu1.add(
        MenuItem(u'测试自定义Key', MENU_TYPE.CLICK, key='testkey'),
        MenuItem(u'测试链接', MENU_TYPE.VIEW, url='http://wx.hdget.com/admin/test/'),
        MenuItem(u'扫码推事件', MENU_TYPE.SCANCODE_PUSH, key=MENU_TYPE.SCANCODE_PUSH),
        MenuItem(u'扫码带提示', MENU_TYPE.SCANCODE_WAITMSG, key=MENU_TYPE.SCANCODE_WAITMSG),
        MenuItem(u'发送位置', MENU_TYPE.LOCATION_SELECT, key=MENU_TYPE.SCANCODE_PUSH),
    )
    menu2 = SubMenu(u'测试二')
    menu2.add(
        MenuItem(u'系统拍照发图', MENU_TYPE.PIC_SYSPHOTO, key=MENU_TYPE.PIC_SYSPHOTO),
        MenuItem(u'拍照或相册发图', MENU_TYPE.PIC_PHOTO_OR_ALBUM, key=MENU_TYPE.PIC_PHOTO_OR_ALBUM),
        MenuItem(u'微信相册发图', MENU_TYPE.PIC_WEIXIN, key=MENU_TYPE.PIC_WEIXIN),
        #MenuItem(u'发送图片', MENU_TYPE.MEDIA_ID, media_id='1BJ-pItyz_QAbg-_pGnW5QXSNJGU5DddfZBoy3lVXstaseStfpFjXG84Y3eTPIF8'),
        #MenuItem(u'发送图文消息', MENU_TYPE.VIEW_LIMITED, media_id=MENU_TYPE.VIEW_LIMITED),
    )
    menu3 = SubMenu(u'Web测试')
    menu3.add(
        MenuItem(u'个人中心', MENU_TYPE.VIEW,
                     url='http://wx.hdget.com/apps/member/'),
        MenuItem(u'绑定账号', MENU_TYPE.VIEW,
                     url='http://wx.hdget.com/apps/member/bind/'),
    )

    menu_config.add(menu1, menu2, menu3)
    menu_config_dict = menu_config.to_dict()

    result = client.send_task('api.menu.create', (menu_config_dict,))
    print result.get()

