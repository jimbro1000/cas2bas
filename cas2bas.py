import sys

import Cas_Format
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
            if sys.argv[2] == "-dd" or sys.argv == "--dragondos":
                self.mode = 1
        if self.mode == 0:
            tokeniser = Dragon_Tokens.DragonToken()
        else:
            tokeniser = Dragon_Tokens.DragonDosToken()
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
