import sys
import json
from os.path import join, splitext, basename

from cas2bas.cas_format import CasFormat, LEADER
from cas2bas.coco_tokens import CoCoToken, RsDosToken
from cas2bas.dragon_tokens import DragonToken, DragonDosToken


def usage():
    print("Dragon CAS format to BASIC listing")
    print("Version 1.0.2")
    print("Usage:")
    print("  cas2bas [input_filename] [output_filename] [options] ")
    print("Options:")
    print("  -dd --dos     : use DragonDos extended BASIC")
    print("  -cc --coco    : use Coco BASIC")
    print("  -rd --rsdos   : use Coco Rsdos extended BASIC")
    print("  -v  --verbose : print debugging messages")


def leader_bytes(filedata, filter=True):
    """
    Get the start index of all strings of leaders in the file
    and the number of leader bytes in that sequence
    This is because there's lots of really short leader sequences that
    are probably just random noise.

    `filter` removes all sequences that are less than 128 bytes
    (http://www.cs.unc.edu/~yakowenk/coco/text/tapeformat.html)
    """
    all_leaders = [i for i, val in enumerate(filedata) if val == LEADER]

    diff = [all_leaders[i + 1] - all_leaders[i]
            for i, val in enumerate(all_leaders) if val != all_leaders[-1]] + [0]

    start_bytes = []
    seq_lengths = []
    l = 1
    for i, d in zip(all_leaders, diff):
        if d != 1:
            if not filter or l > 128:
                start_bytes.append(i - l + 1)
                seq_lengths.append(l)
            l = 1
        else:
            l += 1

    return(start_bytes, seq_lengths)


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
        filename_noext = splitext(basename(filename))[0]  # For output files
        output_path = sys.argv[2]
        opts = sys.argv[3:]
        if len(opts) > 0:
            if any([op in ["-v", "--verbose"] for op in opts]):
                self.verbose = True
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

        # Get "LEADER" byte indices
        leader_seq_idx, leader_length = leader_bytes(filedata)

        # Listing of programs (including ones that got corrupted)
        # TODO: Modification (or parameter) of Cas_Format that attempts to
        # recover as much as possible.
        program_dict = {"program": [], "byte_index": [], "success": []}
        last_byte = -1  # to be updated in the loop

        # Extract, starting at each place a string of leader bytes starts
        for idx, l in zip(leader_seq_idx, leader_length):
            if idx < last_byte:
                continue

            formatter = CasFormat(
                filedata, tokeniser, idx, verbose=self.verbose)
            result = formatter.process_header()

            if result == 0:
                result = formatter.process_file()
                # Write output
                output = join(output_path, f"{idx}_{formatter.file_name}.BAS")
                program_dict['byte_index'].append(idx)
                program_dict['program'].append(formatter.file_name)
                # Only try to write if string was actually produced
                if isinstance(result, str):
                    with open(output, "w") as f:
                        f.write(result)
                    program_dict['success'].append(1)
                    print(
                        f"{output} extracted from {filename} using \033[1m{tokeniser.name}\033[0m")
                    # Save last byte index to prevent trying to read from the
                    # middle of this program
                    last_byte = formatter.byte_index

                else:
                    program_dict['success'].append(0)
                    print(f"Unable to write {output}")
            else:
                print(
                    f"Sequence starting at byte {idx} produced the error above.")

        # Write dict
        with open(join(output_path, 'programs.json'), 'w') as f:
            json.dump(program_dict, f)


def main():
    app = Main()
    app.run()


if __name__ == "__main__":
    exec()
