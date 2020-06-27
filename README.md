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

Optionally you can provide a `-dd` or `--dragondos` option after the filename to use 
the DragonDos extended BASIC tokens

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
 