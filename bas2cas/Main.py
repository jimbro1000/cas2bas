import sys

from formats.Tokeniser_Factory import find_tokeniser
from formats.Utility import find_verbosity


def usage():
    print("Dragon ASCII BASIC listing to CAS format")
    print("Version 2.0.0")
    print("Usage:")
    print("  bas2cas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -dd --dragondos : use DragonDos extended BASIC")
    print("  -cc --coco      : use Coco BASIC")
    print("  -rd --rsdos     : use Coco Rsdos extended BASIC")
    print("If none of the token options are given, Dragon tokens are used")
    print("  -s --silent     : suppress all console output")
    print("  -q --quiet      : only show errors in console")
    print("  -v --verbose    : show all messages")
    print("Default messages are informational only")


class Main(object):

    def __init__(self):
        self.result = ""
        self.mode = 0
        self.verbose = 1

    def run(self) -> object:
        # Process parameters
        if len(sys.argv) < 3:
            usage()
            return
        filename = sys.argv[1]
        output = sys.argv[2]
        tokeniser = find_tokeniser(sys.argv[3:])
        self.verbosity = find_verbosity(sys.argv[3:])
        # Read file
        with open(filename, "rb") as sourceFile:
            filedata = sourceFile.read()


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
