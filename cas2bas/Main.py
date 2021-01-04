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
    print("If none of the options are specified, Dragon tokens will be used.")


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


def initialise_formatter(filename, tokeniser):
    with open(filename, "rb") as sourceFile:
        file_data = sourceFile.read()
    return CasFormat(file_data, tokeniser)


class Main(object):

    def __init__(self):
        self.result = ""
        self.verbose = False

    def run(self) -> object:
        # Process parameters
        if len(sys.argv) < 3:
            usage()
            return
        filename = sys.argv[1]
        output = sys.argv[2]
        tokeniser = find_tokeniser(sys.argv[3:])
        formatter = initialise_formatter(filename, tokeniser)
        header = formatter.process_header()
        # Process the code
        if header == 0:
            print(f"Located program {formatter.file_name}")
            result = formatter.process_file()
            # Only try to write if string was actually produced
            if isinstance(result, str):
                with open(output, "w") as f:
                    f.write(result)
                print(
                    f"{output} extracted from {filename} using \033[1m{tokeniser.name}\033[0m")

            else:
                print("Processing file failed")
                raise Exception
        else:
            print("Processing header failed")
            raise Exception


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
