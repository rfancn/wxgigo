class WXMPCode(object):
    SUCCESS = 0

#########################################################################
# Weixin Security Module Error Definition
#########################################################################
    #  校验签名失败
    ERR_VALIDATE_SIGNATURE = -40001
    # 解析xml失败
    ERR_PARSE_XML = -40002
    # 计算签名失败
    ERR_CALCULATE_SIGNATURE = -40003
    # 不合法的AESKey
    ERR_INVALID_AES_KEY = -40004
    # 校验AppID失败
    ERR_VERITY_APP_ID = -40005
    # AES加密失败
    ERR_ENCRYPT_AES = -40006
    # AES解密失败
    ERR_DECRYPT_AES = -40007
    # 公众平台发送的xml不合法
    ERR_INVALID_XML_MSG = -40008
    # Base64编码失败
    ERR_ENCODE_BASE64 = -40009
    # Base64解码失败
    ERR_DECODE_BASE64 = -40010
    # 公众帐号生成回包xml失败
    ERR_GENERATE_XML = -40011

