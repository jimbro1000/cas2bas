import sys

from formats.Cas_Format import CasFormat, BASIC_FILE_IDENTIFIER, \
    BINARY_FILE_IDENTIFIER
from formats.Tokeniser_Factory import find_tokeniser
from formats.Utility import find_verbosity, find_program_name, \
    find_binary_flag


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 2.2.1")
    print("Usage:")
    print("  cas2bas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -p [program_name] : extract named program from CAS file")
    print("  -b  --binary      : extract a binary file")
    print("  -dd --dragondos   : use DragonDos extended BASIC")
    print("  -cc --coco        : use Coco BASIC")
    print("  -rd --rsdos       : use Coco RSDos extended BASIC")
    print("  -b2 --basic2      : use TRS80 BASIC II")
    print("If none of the token options are given, Dragon tokens are used")
    print("  -s --silent       : suppress all console output")
    print("  -q --quiet        : only show errors in console")
    print("  -v --verbose      : show all messages")
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
        self.program = None
        self.binary = False

    def run(self) -> object:
        # Process parameters
        if len(sys.argv) < 3:
            usage()
            return
        self.filename = sys.argv[1]
        self.output = sys.argv[2]
        tokeniser = find_tokeniser(sys.argv[3:])
        self.verbosity = find_verbosity(sys.argv[3:])
        self.program = find_program_name(sys.argv[3:])
        self.binary = find_binary_flag(sys.argv[3:])
        self.report(0, f"Using {tokeniser.name}")
        formatter = initialise_formatter(
            self.filename, tokeniser, self.verbosity
        )
        self.process_cas(formatter)

    def file_id(self):
        """The file type being extracted, binary if the flag is set."""
        if self.binary:
            return BINARY_FILE_IDENTIFIER
        return BASIC_FILE_IDENTIFIER

    def process_cas(self, formatter):
        if self.program is None:
            header = formatter.process_header(file_id=self.file_id())
        else:
            header = self.find_program(formatter)
        # Process the code
        if header == 0:
            self.report(1, f"Located program {formatter.file_name}")
            if self.binary:
                self.result = formatter.process_binary()
                result_type, mode = bytes, "wb"
            else:
                self.result = formatter.process_file()
                result_type, mode = str, "w"
            # Only try to write if a result was actually produced
            if isinstance(self.result, result_type):
                with open(self.output, mode) as f:
                    f.write(self.result)
                message = f"{self.output} extracted from {self.filename}"
                if not self.binary:
                    message += \
                        f" using \033[1m{formatter.tokeniser.name}\033[0m"
                self.report(1, message)
                sys.exit(0)
            else:
                self.report(2, "Processing file failed")
                sys.exit(1)
        else:
            self.report(2, "Processing header failed")
            sys.exit(1)

    def find_program(self, formatter):
        """Skips segments in the stream until the named program is found.
        Segments of other types are skipped unless they are the named
        program. Returns 0 with the formatter positioned at the program
        data, or -1 if the program is not present, is not of the type
        being extracted (basic or binary) or the stream is invalid."""
        wanted = self.program.replace(" ", "")[:8]
        while True:
            header = formatter.process_header(
                report_errors=False, file_id=self.file_id())
            if formatter.header_end is None:
                # could not locate a name block at all
                self.report(2, formatter.header_error)
                return -1
            if formatter.file_name == wanted:
                if header != 0:
                    self.report(2, formatter.header_error)
                return header
            self.report(1, f"Skipped program {formatter.file_name}")
            if formatter.skip_file() != 0 or not formatter.has_next_file():
                self.report(2, f"Program {self.program} not found")
                return -1
            formatter.reset_file()

    def report(self, level, message):
        if level >= self.verbosity:
            print(message)


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
