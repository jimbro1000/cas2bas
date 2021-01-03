import sys

PENDING = 0
EXPECTING_LINE_ADDRESS_HIGH = 1
EXPECTING_LINE_ADDRESS_LOW = 2
EXPECTING_LINE_NUMBER_HIGH = 3
EXPECTING_LINE_NUMBER_LOW = 4
LINE_DATA = 5
FAILED = -1
LEADER = 0x55
SYNC = 0x3C
NAME_FILE_BLOCK = 0x00
DATA_BLOCK = 0x01
END_OF_FILE_BLOCK = 0xFF
BASIC_FILE_IDENTIFIER = 0x00
DATA_FILE_IDENTIFIER = 0x01
BINARY_FILE_IDENTIFIER = 0x02
ASCII_FILE_FLAG = 0xFF
BINARY_FILE_FLAG = 0x00
CONTINUOUS_FILE = 0x00


class CasFormat(object):
    """Processes a file stream of byte data according to the CAS format for BASIC source code."""

    def __init__(self, filedata, tokeniser):
        self.state = PENDING
        self.tokeniser = tokeniser
        self.data = filedata
        self.state = -1
        self.byte_index = 0
        self.file_name = ""
        self.current_line = ""
        self.listing = []
        self.line_number = 0
        self.next_line = 0
        self.exec_address = 0
        self.load_address = 0

    def next_byte(self):
        """Provides the next byte from the loaded byte array.
        This is a forward only operation."""
        if self.byte_index < len(self.data):
            value = self.data[self.byte_index]
            self.byte_index += 1
            return value
        else:
            print("file length exceeded (" + str(self.byte_index) +
                  " of " + str(len(self.data)) + ")")
            sys.exit(-1)

    def process_header(self):
        """Processes the file header to verify file type and find file data start point."""
        head = self.next_byte()
        leader_length = 0
        while head == LEADER:
            leader_length += 1
            head = self.next_byte()
        if head != SYNC:
            print("unknown file type, invalid sync byte: " + str(head))
            return -1
        head = self.next_byte()
        if head != NAME_FILE_BLOCK:
            print("illegal file type")
            return -1
        self.next_byte()
        # header length - don't need it
        # self.next_byte()
        # this byte is unidentified
        head = self.next_byte()
        name_index = 0
        while name_index < 8:
            if head != 0x20:
                self.file_name += chr(head)
            head = self.next_byte()
            name_index += 1
        # file id  byte
        if head != BASIC_FILE_IDENTIFIER:
            print("not a basic listing")
            return -1
        head = self.next_byte()
        # ascii flag
        if head != ASCII_FILE_FLAG and head != BINARY_FILE_FLAG:
            print("not a valid byte format - must be ascii or binary")
            return -1
        head = self.next_byte()
        # gap flag
        if head != CONTINUOUS_FILE:
            print("not a continuous file")
            return -1
        head = self.next_byte()
        # exec address
        self.exec_address = head
        head = self.next_byte()
        self.exec_address = self.exec_address * 256 + head
        head = self.next_byte()
        # load address
        self.load_address = head
        head = self.next_byte()
        self.load_address = self.load_address * 256 + head
        self.next_byte()
        # this byte is unidentified
        self.state = EXPECTING_LINE_ADDRESS_HIGH
        return 0

    def process_file(self):
        """Processes the file body to extract the token stream.
        File is in blocks so operates as a block iterator with the content being processed in a slim state machine."""
        head = self.next_byte()
        while head == LEADER:
            head = self.next_byte()
        if head != SYNC:
            print("unknown file type, invalid sync byte: " + str(head))
            return -1
        head = self.next_byte()
        while head == DATA_BLOCK:
            head = self.next_byte()
            length = head
            head = self.next_byte()
            while length > 0:
                length -= 1
                self.build_listing(head)
                head = self.next_byte()
            # skip checksum byte
            head = self.next_byte()
            # process two leaders
            if head != LEADER:
                print("invalid block leader")
                return -1
            head = self.next_byte()
            if head != LEADER:
                print("invalid block leader")
                return -1
            head = self.next_byte()
            if head != SYNC:
                print("unknown file type")
                return -1
            head = self.next_byte()
        if head != END_OF_FILE_BLOCK:
            print("invalid end of file block")
            return -1
        self.state = 100
        return self.generate_final_listing()

    def build_listing(self, next_byte):
        """Turns block contents into a string formatted, de-tokenised list"""
        def next_line_high():
            self.next_line = next_byte * 256
            self.state = EXPECTING_LINE_ADDRESS_LOW

        def next_line_low():
            self.next_line += next_byte
            self.state = EXPECTING_LINE_NUMBER_HIGH

        def line_number_high():
            self.line_number = next_byte * 256
            self.state = EXPECTING_LINE_NUMBER_LOW

        def line_number_low():
            self.line_number += next_byte
            self.current_line = str(self.line_number) + " "
            self.state = LINE_DATA

        def process_byte():
            if next_byte == 0:
                self.current_line += chr(10) + chr(13)
                self.listing.append(self.current_line)
                self.current_line = ""
                self.state = EXPECTING_LINE_ADDRESS_HIGH
            else:
                self.current_line += self.tokeniser.convert(next_byte)

        if self.state == EXPECTING_LINE_ADDRESS_HIGH:
            next_line_high()
        elif self.state == EXPECTING_LINE_ADDRESS_LOW:
            next_line_low()
        elif self.state == EXPECTING_LINE_NUMBER_HIGH:
            line_number_high()
        elif self.state == EXPECTING_LINE_NUMBER_LOW:
            line_number_low()
        elif self.state == LINE_DATA:
            process_byte()

    def generate_final_listing(self):
        """Turns the list of lines into a single string."""
        result = ""
        return result.join(self.listing)
