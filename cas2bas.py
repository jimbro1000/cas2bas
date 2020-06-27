import sys

import Cas_Format
import Dragon_Tokens


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 1.0.2")
    print("Usage:")
    print("cas2bas [filename]")


class Main(object):

    def __init__(self):
        self.result = ""

    def run(self):
        if len(sys.argv) != 2:
            usage()
            return
        filename = sys.argv[1]
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
