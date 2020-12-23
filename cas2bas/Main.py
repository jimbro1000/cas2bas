import sys
import json
from os.path import join, splitext, basename

from cas2bas.Cas_Format import CasFormat, LEADER
from cas2bas.Coco_Tokens import CoCoToken, RsDosToken
from cas2bas.Dragon_Tokens import DragonToken, DragonDosToken


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 1.0.2")
    print("Usage:")
    print("  cas2bas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -dd --dos     : use DragonDos extended BASIC")
    print("  -cc --coco    : use Coco BASIC")
    print("  -rd --rsdos   : use Coco Rsdos extended BASIC")
    print("If none of the options are specified, Dragon tokens will be used.")


class Main(object):

    def __init__(self):
        self.result = ""
        self.mode = 0
        self.verbose = False

    def run(self):
        # Process parameters
        if len(sys.argv) < 3:
            usage()
            return
        filename = sys.argv[1]
        output = sys.argv[2]
        opts = sys.argv[3:]
        if len(opts) > 0:
            if any([op in ["-dd", "--dragondos"] for op in opts]):
                self.mode = 1
            elif any([op in ["-cc", "--coco"] for op in opts]):
                self.mode = 2
            elif any([op in ["-rd", "--rsdos"] for op in opts]):
                self.mode = 3
        if self.mode == 1:
            tokeniser = DragonDosToken()
        elif self.mode == 2:
            tokeniser = CoCoToken()
        elif self.mode == 3:
            tokeniser = RsDosToken()
        else:
            tokeniser = DragonToken()
        # Read file
        with open(filename, "rb") as sourceFile:
            filedata = sourceFile.read()
        # Look at file header
        formatter = CasFormat(
            filedata, tokeniser)
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
