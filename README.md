# README #

### What is this repository for? ###

This project provides a quick (and dirty) method of extracting tokenised BASIC code from a Dragon CAS format file

While tested against a variety of files there are no guarantees that it will work for everything given the potential
abuses of the file format

#### New Features in V2 ####

An experimental version of the code that converts untokenised ASCII text to CAS format is available using the bas2cas
command. See [bas2cas](#bas2cas)

### How do I get set up? ###

* Python interpreter (almost any version will do)
* Either pip, [pipx](https://pipxproject.github.io/pipx/), or clone the repository to your local computer (see
  [instructions](#instructions))
* Some suitable BASIC CAS files

## Instructions ##

There are a few options for getting the script working.

### Using pipx ###

If you use [pipx](https://pipxproject.github.io/pipx/) you can run

```pipx install git+https://github.com/jimbro1000/cas2bas.git@development```

after which `cas2bas` will be available as a command line program. You can use it with

```cas2bas input.cas output.bas```

Also see [Parameters](#parameters).

### As local script ###

To use the script locally just run

```python cas2bas.py input.cas output.bas```

Also see [Parameters](#parameters).

## Parameters ##

The output will be a formatted text listing of the contained BASIC code, or the raw contents of a binary file if `-b` is used

If there are any format errors in the CAS file the script will exit with an error code and description.

  `-p [program_name]` extracts the named program instead of the first program

  `-b --binary` extracts a binary (machine code) file instead of a BASIC listing

  `-dd --dragondos` uses Dragon and DragonDos tokens

  `-cc --coco` uses CoCo instead of Dragon tokens

  `-rd --rsdos` uses CoCo and RsDos tokens

Additionally the earlier Basic II tokens can be used (this is an experimental feature)

  `-b2 --basic2` uses the Trs80 Basic II tokens instead of Dragon tokens

for example:
```
cas2bas input.cas output.bas --coco
```
will attempt to convert the contents of input.cas to output.bas using the CoCo color basic tokens

### Binary Files ###

When `-b` is given the program must be a binary file (file ID 02 in the namefile block), otherwise the converter exits with an error. Other programs in the CAS file are skipped when `-p` is used to name the binary file.

The output file is written as raw bytes:

1. Two bytes for the EXEC address (high byte first)
2. Two bytes for the load address (high byte first)
3. The contents of all data blocks as a single contiguous stream

for example:
```
cas2bas input.cas output.bin -b -p GAME
```
will extract the binary file GAME from input.cas to output.bin

### Reporting ###

By default the converter will confirm the operation and outcome but this can be modified

  `-q --quiet` will reduce output to just errors

  `-s --silent` will supress all console output

  `-v --verbose` will increase console output to include all activity

## Running Tests ##

Install libraries from pip using ```pip install -r requirements.txt```

Unit tests are composed in pytest, to run the test suite use ```pytest``` from the project root

## Compatibility ##

The tokens used are the standard Microsoft Extended Color Basic tokens and should work a COCO CAS file but this is
untested and may give confusing results

The script is set to treat binary and ASCII files in the same way but this assumption has the potential to cause issues

Many commercial packages, while written in basic, used a memory dump to achieve an autorun of BASIC code. If you want a
listing of such a file you will need to load it as normal, perform a soft reset and then save the code again as a BASIC
file

## bas2cas ##

A new feature in version 2 is the ability to reverse the conversion process and turn plain text BASIC code into the
tokenised format held in .cas files.

Operation of the bas2cas command is essentially the same as the cas2bas command with the input being plain text (bas)
and the output being cassette format (cas).

### bas2cas parameters ###

Control parameters are the same with a few additions:

  `-h --header xx` will set the length of cassette file header to the following value. 
  By default the length is set at 128 bytes. Valid values are 1 to 65535.

  `-b --base xx` modifies the base address of the code. By default the base address is `0x1e00`. Any 16 bit value is 
  accepted but validity will depend on the target hardware. The supplied value can be decimal or hexadecimal using the 
  0x prefix.

In both cases values outside of the accepted ranges will be rejected and the default used instead.

## CAS File Format ##

From [WorldOfDragon](http://www.archive.worldofdragon.org/index.php?title=Tape%5CDisk_Preservation#CAS_File_Format)

The CAS file format was originally created for the PC-Dragon emulator and is one way of representing programs or data stored on Dragon cassette tapes. The CAS file format comes in two flavours, the most usual and default format is modelled after how the Dragon actually stores data on cassettes, optionally with truncated leader bytes to minimise the file size. The alternate format is simply the RAW bit stream and was only used for games that did not conform to the standard tape format (an early form of copy protection).

The standard Dragon tape format is:

1. A leader block of $55 multiplied by the 16 bit number in location $90:91 (default 128). 
2. A namefile block. 
3. A blank section of tape for processing of the namefile block. 
4. Another leader block of $90:91 bytes of $55 
5. One or more data blocks. 
6. An end-of-file block.

A header block, data block or EOF file block consists of:

1. A leader byte - $55 
2. A sync byte - $3C 
3. A block type byte:

                     00=namefile block
                     01=data block
                     FF=end-of-file block
4. A block length byte (0-255)

5. 0-255 bytes of data. For a namefile block this consists of:
```
    5.1 An 8 byte program name
    5.2 A file ID byte where:
        00=BASIC program
        01=Data file
        02=Binary file
    5.3 An ASCII flag where:
        00=Binary file
        FF=ASCII file
    5.4 A gap flag to indicate whether the
        data stream is continuous (00) as
        in binary or BASIC files, or in blocks
        where the tape keeps stopping (FF) as
        in data files.
    5.5 Two bytes for the default EXEC address
        of a binary file.
    5.6 Two bytes for the default load address
        of a binary file.
```
For a data block, this consists of the actual data to load/save and there is no data associated with an EOF block.

6. A checksum byte which is: sum of all the data bytes + block type + block length.

7. A trailer byte - $55


The first byte of a CAS file must be $55 for identification purposes. The first block of a standard format CAS file should be a namefile block, and the last block is usually an EOF block. Some games used copy protection where the number of blocks to be loaded did not match the number specified in the file header and a fake EOF block was included so that a simple copy of the file would result in a truncated file (other similar mechanisms skipped blocks or used non-standard block types).

Note that standard format CAS files may omit leaders. If leaders are required, use the FIXCAS utility to add leaders to more closely resemble the true Dragon cassette tape format. Since the standard format CAS file is a fairly simple representation of the data stream read from a tape after demodulation and decoding of the audio signals, certain properties of cassette tapes cannot be reproduced, e.g. gaps of silence (at least one game loader uses this as a copy protection mechanism that needs the RAW format of CAS to work - although this doesn't store silence it does store noise in those gaps).

The above description makes it pretty easy to create CAS files. Reading CAS files can be a bit more difficult though. Data is actually represented as a stream of bits on cassette tapes, and the Dragon uses different audio signals to represent different bit values. When decoding such an audio signal into a bit stream and creating a CAS file, the structure described above might not align to byte boundaries in the CAS file (this can occur when using DC, although DCWIN does synchronise bitstream conversions to byte boundaries). Especially the leader may not be decoded to an integral number of bytes. To make matters even worse, both leaders and sync bytes may contain noise and still be readable. A robust CAS file reader must take this into account.

## Credits ##

While I started out doing this on my own there have been a few helping hands along the way:

* Daniel Farnand for making me invest some more time in the tools and stretching the ideas
* Mike Miller (facebook) for pointing me in the right direction to Walter K. Zydhek's work on the find detail of
  Microsoft Color Basic
* Ciaran Anscomb for maintaining the incredibly useful XROAR emulator
