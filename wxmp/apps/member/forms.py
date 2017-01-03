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
from django import forms

class BindForm(forms.Form):
    telephone = forms.CharField(label=u'手机号码', help_text='请输入正确手机号码', max_length=11)
    vcode = forms.CharField(label=u'验证码', help_text='请输入验证码', max_length=6)


    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        try:
            int(telephone)
        except:
            raise forms.ValidationError("Invalid telephone number!")

        if len(telephone.strip()) != 11:
            raise forms.ValidationError("Invalid telephone number!")

        return telephone

    def clean_vcode(self):
        vcode = self.cleaned_data['vcode']
        if vcode != '123456':
            raise forms.ValidationError("Failed to verfiy vcode!")

        return vcode
