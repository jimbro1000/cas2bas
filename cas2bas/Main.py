import sys

from formats.Cas_Format import CasFormat
from formats.Tokeniser_Factory import find_tokeniser
from formats.Utility import find_verbosity


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 2.0.0")
    print("Usage:")
    print("  cas2bas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -dd --dragondos : use DragonDos extended BASIC")
    print("  -cc --coco      : use Coco BASIC")
    print("  -rd --rsdos     : use Coco RSDos extended BASIC")
    print("  -b2 --basic2    : use TRS80 BASIC II")
    print("If none of the token options are given, Dragon tokens are used")
    print("  -s --silent     : suppress all console output")
    print("  -q --quiet      : only show errors in console")
    print("  -v --verbose    : show all messages")
    print("Default messages are informational only")


def initialise_formatter(filename, tokeniser, verbosity):
    with open(filename, "rb") as sourceFile:
        file_data = sourceFile.read()
    return CasFormat(file_data, tokeniser, verbosity)


class Main(object):

    def __init__(self):
        self.result = ""
        self.verbosity = 1
        self.filename = ""
        self.output = ""

    def run(self) -> object:
        # Process parameters
        if len(sys.argv) < 3:
            usage()
            return
        self.filename = sys.argv[1]
        self.output = sys.argv[2]
        tokeniser = find_tokeniser(sys.argv[3:])
        self.verbosity = find_verbosity(sys.argv[3:])
        self.report(0, f"Using {tokeniser.name}")
        formatter = initialise_formatter(
            self.filename, tokeniser, self.verbosity
        )
        self.process_cas(formatter)

    def process_cas(self, formatter):
        header = formatter.process_header()
        # Process the code
        if header == 0:
            self.report(1, f"Located program {formatter.file_name}")
            self.result = formatter.process_file()
            # Only try to write if string was actually produced
            if isinstance(self.result, str):
                with open(self.output, "w") as f:
                    f.write(self.result)
                self.report(
                    1,
                    f"{self.output} extracted from {self.filename} \
using \033[1m{formatter.tokeniser.name}\033[0m"
                )
            else:
                self.report(2, "Processing file failed")
                raise Exception
        else:
            self.report(2, "Processing header failed")
            raise Exception

    def report(self, level, message):
        if level >= self.verbosity:
            print(message)


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
