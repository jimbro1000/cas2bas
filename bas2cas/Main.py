import sys

from formats.Coco_Tokens import CoCoToken, RsDosToken
from formats.Dragon_Tokens import DragonToken, DragonDosToken


def usage():
    print("Dragon ASCII BASIC listing to CAS format")
    print("Version 2.0.0")
    print("Usage:")
    print("  bas2cas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -dd --dragondos : use DragonDos extended BASIC")
    print("  -cc --coco      : use Coco BASIC")
    print("  -rd --rsdos     : use Coco Rsdos extended BASIC")
    print("If none of the options are specified, Dragon tokens will be used.")


class Main(object):

    def __init__(self):
        self.result = ""
        self.mode = 0
        self.verbose = False

    def run(self) -> object:
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


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
