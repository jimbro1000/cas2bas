import sys

import Cas_Format


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Usage:")
    print("cas2bas [filename]")


class Main(object):

    def __init__(self):
        self.result = ""

    def run(self):
        if len(sys.argv) != 2:
            usage()
            return
        self.input = sys.argv[1]
        formatter = Cas_Format.CasFormat(self.input)
        result = formatter.process_header()
        if result == 0:
            result = formatter.process_file()
        print(result)


if __name__ == "__main__":
    app = Main()
    app.run()
