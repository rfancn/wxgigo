
class PKCS7Encoder(object):
    """
    reference:
    * http://tools.ietf.org/html/rfc2315
    * http://programmerin.blogspot.jp/2011/08/python-padding-with-pkcs7.html
    """
    class InvalidBlockSizeError(Exception):
        """Raised for invalid block sizes"""
        pass

    def __init__(self, blockSize=32):
        if blockSize < 2 or blockSize > 255:
            raise PKCS7Encoder.InvalidBlockSizeError("The block size must be between 2 and 255, inclusive")

        self.blockSize = blockSize

    def encode(self, rawText):
        textLen = len(rawText)
        amountToPad = self.blockSize - (textLen % self.blockSize)
        if amountToPad == 0:
            amountToPad = self.blockSize
        pad = chr(amountToPad)
        return rawText + pad * amountToPad

    def decode(self, encodedText):
        pad = ord(encodedText[-1])
        if pad < 1 or pad > 32:
            pad = 0

        return encodedText[:-pad]
