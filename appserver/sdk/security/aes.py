class AESCipher(object):
    """
    ref: http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    """
    def __init__(self, key, appId):
        self.appId = appId
        self.aes = AES.new(key, AES.MODE_CBC, key[:16])
        self.pkcs7 = PKCS7Encoder()

    def encrypt(self, rawText):
        """
        usermsg encrypt algorithm:
        Base64_Encode(AES_Encrypt [random(16B)+ msg_len(4B) + usermsg + $AppId])
        """
        encryptedText = None
        try:
            # represent Python values to C structs: I -> unsigned integer, ! -> network byte order
            MSGLEN = lambda s: struct.pack("!I", len(s))
            # assmbly formatted text
            formattedText  =  Random.new().read(16) + MSGLEN(rawText) + rawText + self.appId
            # pkcs#7 padding
            paddedText = self.pkcs7.encode(formattedText)
            encryptedText = base64.b64encode(self.aes.encrypt(paddedText))
        except Exception,e:
            return  WXCode.ERR_ENCRYPT_AES, None

        return WXCode.SUCCESS, encryptedText

    def decrypt(self, encryptedText):
        paddedText = None
        try:
            paddedText  = self.aes.decrypt(base64.b64decode(encryptedText))
        except Exception,e:
            return  WXCode.ERR_DECRYPT_AES, None

        rawText = None
        originalAppId = None
        try:
            # formatted_text: random(16B)+ msg_len(4B) + usermsg + $AppId
            formattedText = self.pkcs7.decode(paddedText)
            MSGLEN = lambda x : struct.unpack("!I", x)
            rawTextLen = MSGLEN(formattedText [16:20])[0]
            rawText = formattedText[20:(20+rawTextLen)]
            originalAppId = formattedText[(20+rawTextLen):]
        except Exception,e:
            return WXCode.ERR_INVALID_XML_MSG

        if  originalAppId != self.appId:
            return WXCode.ERR_VERITY_APP_ID, None

        return WXCode.SUCCESS, rawText
