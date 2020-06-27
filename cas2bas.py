import sys

import Cas_Format
import Coco_Tokens
import Dragon_Tokens


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 1.0.2")
    print("Usage:")
    print("  cas2bas [filename] [options]")
    print("Options:")
    print("  -d --dos : use DragonDos extended BASIC")


class Main(object):

    def __init__(self):
        self.result = ""
        self.mode = 0

    def run(self):
        if len(sys.argv) < 2:
            usage()
            return
        filename = sys.argv[1]
        if len(sys.argv) > 2:
            if sys.argv[2] == "-dd" or sys.argv[2] == "--dragondos":
                self.mode = 1
            if sys.argv[2] == "-cc" or sys.argv[2] == "--coco":
                self.mode = 2
            if sys.argv[2] == "-rd" or sys.argv[2] == "--rsdos":
                self.mode = 3
        if self.mode == 1:
            tokeniser = Dragon_Tokens.DragonDosToken()
        elif self.mode == 2:
            tokeniser = Coco_Tokens.CoCoToken()
        elif self.mode == 3:
            tokeniser = Coco_Tokens.RsDosToken()
        else:
            tokeniser = Dragon_Tokens.DragonToken()
        sourceFile = open(filename, "rb")
        filedata = sourceFile.read()
        sourceFile.close()
        formatter = Cas_Format.CasFormat(filedata, tokeniser)
        result = formatter.process_header()
        if result == 0:
            result = formatter.process_file()
        print(result)


if __name__ == "__main__":
    app = Main()
    app.run()
