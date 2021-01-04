import sys

from formats.Cas_Format import CasFormat
from formats.Coco_Tokens import CoCoToken, RsDosToken
from formats.Dragon_Tokens import DragonToken, DragonDosToken


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 2.0.0")
    print("Usage:")
    print("  cas2bas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -dd --dragondos : use DragonDos extended BASIC")
    print("  -cc --coco      : use Coco BASIC")
    print("  -rd --rsdos     : use Coco RSDos extended BASIC")
    print("If none of the token options are specified, Dragon tokens will be used.")
    print("  -s --silent     : suppress all console output")
    print("  -q --quiet      : only show errors in console")
    print("  -v --verbose    : show all messages")
    print("Default messages are informational only")


def find_tokeniser(options):
    result = DragonToken()
    if len(options) > 0:
        if any([op in ["-dd", "--dragondos"] for op in options]):
            result = DragonDosToken()
        elif any([op in ["-cc", "--coco"] for op in options]):
            result = CoCoToken()
        elif any([op in ["-rd", "--rsdos"] for op in options]):
            result = RsDosToken()
    return result


def find_verbosity(options):
    result = 1
    if len(options) > 0:
        if any([op in ["-s", "--silent"] for op in options]):
            result = 3
        if any([op in ["-q", "--quiet"] for op in options]):
            result = 2
        if any([op in ["-v", "--verbose"] for op in options]):
            result = 0
    return result


def initialise_formatter(filename, tokeniser):
    with open(filename, "rb") as sourceFile:
        file_data = sourceFile.read()
    return CasFormat(file_data, tokeniser)


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
        formatter = initialise_formatter(self.filename, tokeniser)
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
                self.report(1,
                            f"{self.output} extracted from {self.filename} using \033[1m{formatter.tokeniser.name}\033[0m")

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
