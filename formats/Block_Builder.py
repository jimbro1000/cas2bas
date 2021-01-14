class FileBlock(object):
    MAXIMUM_BLOCK_LENGTH = 258
    IDENTIFIER_LENGTH = 3

    def __init__(self, block_type):
        self.block_type = block_type
        self.content = [0x3c, block_type, 1]

    def append(self, byte):
        if not (isinstance(byte, int)) or \
                byte < 0 or byte > 255 or \
                (byte % 1 != 0):
            exception = ValueError()
            exception.strerror = "non-byte supplied"
            raise exception
        if len(self.content) < self.MAXIMUM_BLOCK_LENGTH:
            self.content.append(byte)
        else:
            exception = ValueError()
            exception.strerror = "exceeded maximum block length"
            raise exception

    def capacity(self):
        return self.MAXIMUM_BLOCK_LENGTH - len(self.content)

    def seal_block(self):
        length = len(self.content) - self.IDENTIFIER_LENGTH
        checksum = 0
        for x in range(length):
            checksum += self.content[x + self.IDENTIFIER_LENGTH]
        checksum += length
        checksum += self.block_type
        self.content[2] = length
        self.content.append(checksum % 256)
        return self.content
