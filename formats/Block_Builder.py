class FileBlock(object):

    def __init__(self, block_type):
        self.block_type = 0
        self.content = [0x3c, block_type, 1]

    def append(self, byte):
        if not (isinstance(byte, int)) or \
                byte < 0 or byte > 255 or \
                (byte % 1 != 0):
            exception = ValueError()
            exception.strerror = "non-byte supplied"
            raise exception
        if len(self.content) < 258:
            self.content.append(byte)
        else:
            exception = ValueError()
            exception.strerror = "exceeded maximum block length"
            raise exception

    def capacity(self):
        return 258 - len(self.content)

    def seal_block(self):
        length = len(self.content) - 3
        checksum = 0
        for x in range(length):
            checksum += self.content[x + 3]
        checksum += length
        checksum += self.block_type
        self.content[2] = length
        self.content.append(checksum % 256)
        return self.content
