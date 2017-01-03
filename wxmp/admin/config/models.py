# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe

MSG_ENCRYPT_METHOD = (
    ('clear', mark_safe('明文模式<p class="help-block">明文模式下，不使用消息体加解密功能，安全系数较低</p>')),
    ('compatible', mark_safe('兼容模式<p class="help-block">兼容模式下，明文、密文将共存，方便开发者调试和维护</p>')),
    ('secret', mark_safe('安全模式<p class="help-block">安全模式下，消息包为纯密文，需要开发者加密和解密，安全系数高</p>')),
)

# Create your models here.
class WXMPConfig(models.Model):
    wx_id = models.CharField(verbose_name='微信ID', max_length=128, help_text=u'复制自：公众号设置->公开信息->微信号')
    wx_original_id = models.CharField(verbose_name='原始ID', max_length=128, help_text=u'复制自：公众号设置->注册信息->原始ID')
    app_id = models.CharField(verbose_name='AppID(应用ID)', max_length=128, help_text=u'复制自：开发者中心->开发者ID->AppID(应用ID)')
    app_key = models.CharField(verbose_name='AppSecret(应用密钥)', max_length=128, help_text=u'复制自：开发者中心->开发者ID->AppSecret(应用密钥)')
    token = models.CharField(verbose_name='Token(令牌)', max_length=128, help_text=u'复制自：开发者中心->服务器配置->Token(令牌)')
    encoding_aes_key = models.CharField(verbose_name='EncodingAESKey(消息加解密密钥)', max_length=128, help_text=u'复制自：开发者中心->服务器配置->EncodingAESKey(消息加解密密钥)')
    msg_encrypt_method = models.CharField(verbose_name='消息加解密方式', max_length=16)

    class Meta:
        db_table = "wxmp_config"