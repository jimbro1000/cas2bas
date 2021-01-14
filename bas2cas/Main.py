import sys

import formats.Cas_Format
from formats.Tokeniser_Factory import find_tokeniser
from formats.Utility import find_verbosity, find_base_load_address, \
    find_header_length

LOAD_ADDRESS = 0x1E00
HEADER_LENGTH = 128


def usage():
    print("Dragon ASCII BASIC listing to CAS format")
    print("Version 2.0.0")
    print("Usage:")
    print(
        "bas2cas [input_filename] [output_filename] [cassette_filename] ["
        "options] ")
    print("Options:")
    print("  -dd --dragondos : use DragonDos extended BASIC")
    print("  -cc --coco      : use Coco BASIC")
    print("  -rd --rsdos     : use Coco Rsdos extended BASIC")
    print("  -b2 --basic2    : use Trs80 Basic II")
    print("If none of the token options are given, Dragon tokens are used")
    print("  -s --silent     : suppress all console output")
    print("  -q --quiet      : only show errors in console")
    print("  -v --verbose    : show all messages")
    print("Default messages are informational only")
    print("  -b --base xxxx  : set base load address (default is 0x1e00)")
    print("  -h --header xx  : set header run length")


class Main(object):

    def __init__(self):
        self.result = ""
        self.mode = 0
        self.verbose = 1

    def run(self) -> object:
        # Process parameters
        if len(sys.argv) < 4:
            usage()
            return
        filename = sys.argv[1]
        output = sys.argv[2]
        coded_filename = sys.argv[3]
        tokeniser = find_tokeniser(sys.argv[4:])
        self.verbosity = find_verbosity(sys.argv[4:])
        load_address = find_base_load_address(sys.argv[4:], LOAD_ADDRESS)
        header_length = find_header_length(sys.argv[4:], HEADER_LENGTH)
        # Read file
        with open(filename, "rb") as sourceFile:
            file_data = sourceFile.read().decode()
        self.report(1, f"Located program {filename}")
        result, token_stream = tokeniser.parse_program(file_data, load_address)
        if result == 0:
            self.report(1, "file successfully encoded")
            formatter = formats.Cas_Format.CasFormat(
                [], tokeniser, self.verbosity
            )
            output_data = formatter.build_file(coded_filename, token_stream,
                                               header_length)
            with open(output, "wb") as f:
                f.write(output_data)
            self.report(1, f"cas file written as {output}")
        else:
            self.report(2, "file processing failed")

    def report(self, level, message):
        if level >= self.verbosity:
            print(message)


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
