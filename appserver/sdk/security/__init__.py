import base64

class WXMPSecurity(object):
    """
    Class for all kinds of security related operation, like sign,encrypt and decrypt Weixin message

    @param token:             Token setup in http://mp.weixin.qq.com
    @param encoding_aes_key:  EncodingAESKey setup in http://mp.weixin.qq.com
    @param app_id:            AppID setup in http://mp.weixin.qq.com
    """
    def __init__(self, wxConfig):
        self.wxConfig = wxConfig
        try:
            key = base64.b64decode(self.wxConfig.WX_ENCODING_AES_KEY + "=")
            assert len(key) == 32
        except Exception,e:
            raise Exception("Invalid EncodingAESKey!")

        self.aesCipher = AESCipher(key, wxConfig.WX_APP_ID)

    def sign(self, msg, nonce=None, timestamp=None):
        """
        Signing message
        """
        signed_msg = None

        if timestamp is None:
            timestamp = str(int(time.time()))

        if nonce is None:
            nonce =  uuid.uuid4()

        try:
            sortlist = [self.token, self.timestamp, self.nonce, msg]
            sortlist.sort()
            signed_msg = hashlib.sha1().update("".join(sortlist)).hexdigest()
        except Exception,e:
            return  WXCode.ERR_CALCULATE_SIGNATURE, None

        return WXCode.SUCCESS, signed_msg

    def encrypt(self, rawText):
        ret, encryptedText = self.aesCipher.encrypt(rawText)
        if ret != WXCode.SUCCESS:
            raise Exception(ret)

        return encryptedText

    def decrypt(self, encryptedText):
        ret, rawText = self.aesCipher.decrypt(encryptedText)
        if ret != WXCode.SUCCESS:
            raise Exception(ret)

        return rawText

    def validateSignature(self, signature, timestamp, nonce):
        tmpArray = [self.wxConfig.WX_TOKEN, timestamp, nonce]
        tmpArray.sort()
        expectedSignature = hashlib.sha1("".join(tmpArray)).hexdigest()

        return signature == expectedSignature
