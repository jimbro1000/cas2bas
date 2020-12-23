# README #

### What is this repository for? ###

This project provides a quick (and dirty) method of extracting tokenised 
BASIC code from a Dragon CAS format file

While tested against a variety of files there are no guarantees that it 
will work for everything given the potential abuses of the file format 

### How do I get set up? ###

* Python interpreter (almost any version will do)
* Either pip, [pipx](https://pipxproject.github.io/pipx/), or the repository to your local computer (see [instructions](#instructions))
* Some suitable BASIC CAS files

## Instructions

There are a few options for getting the script working.

### Using pipx

If you use [pipx](https://pipxproject.github.io/pipx/) you can run

```pipx install git+https://github.com/jimbro1000/cas2bas.git@development```

after which `cas2bas` will be available as a command line program. You can use it with

```cas2bas input.cas output.bas```

Also see [Parameters.](#parameters)

### As local script

To use the script locally just run 

```python cas2bas.py input.cas output.bas```

Also see [Parameters.](#parameters)

## Parameters

The output will be a formatted text listing of the contained BASIC code

If there are any format errors in the CAS file the script will exit with an
error code and description.

Optionally you can provide a `-dd` or `--dragondos` switch after the filename to use 
the DragonDos extended BASIC tokens

For CoCo files use a `-cc` or `--coco` switch for regular basic or use `-rd` or 
`--rsdos` for CoCo extended basic with rsdos

## Running Tests ###

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
 