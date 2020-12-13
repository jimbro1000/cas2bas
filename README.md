This is a fork I made of [this code](https://bitbucket.org/jimbro1000/cas2bas), written by Julian Brown. If you are him, or know how to get in touch with him, please let me know, I'd like to discuss integrating my changes here upstream.

# Changes from original (which README below refers to)

- Now should be run with an output directory, e.g. `python cas2bas.py input.cas output_dir -rd`. The script will attempt to extract all the basic programs saved in that cassette file.
- Code should be accessible as a package, and can be installed with [pipx](https://pipxproject.github.io/pipx/) for easy command-line access.
- Since some programs will fail to load (due to corrupted data), I still wanted to access their names. The script creates `programs.json` in the output directory, which outputs all this info. (Future TODO: code that pulls as much code as possible from these broken programs).

# README #

### What is this repository for? ###

This project provides a quick (and dirty) method of extracting tokenised 
BASIC code from a Dragon CAS format file

While tested against a variety of files there are no guarantees that it 
will work for everything given the potential abuses of the file format 

### How do I get set up? ###

* Python interpreter (almost any version will do)
* PIP (only if you need to run the tests)
* Some suitable BASIC CAS files
* Clone the repository to your local computer

## Instructions ##

To use the script just run ```python cas2bas.py``` followed by the name of
your CAS file

The output will be a formatted text listing of the contained BASIC code

If there are any format errors in the CAS file the script will exit with an
error code and description

Optionally you can provide a `-dd` or `--dragondos` switch after the filename to use 
the DragonDos extended BASIC tokens

For CoCo files use a `-cc` or `--coco` switch for regular basic or use `-rd` or 
`--rsdos` for CoCo extended basic with rsdos

### Running Tests ###

Install libraries from pip using ```pip install -r requirements.txt```

Unit tests are composed in pytest, to run the test suite use ```pytest``` from the
project root

## Compatibility ##

The tokens used are the standard Microsoft Extended Color Basic tokens and
should work a COCO CAS file but this is untested and may give confusing
results

The script is set to treat binary and ASCII files in the same way but this
assumption has the potential to cause issues

Many commercial packages, while written in basic, used a memory dump to 
achieve an autorun of BASIC code. If you want a listing of such a file you
will need to load it as normal, perform a soft reset and then save the 
code again as a BASIC file
 