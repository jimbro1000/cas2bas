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

The output will be a formatted text listing of the contained BASIC code

If there are any format errors in the CAS file the script will exit with an error code and description.

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

## Credits ##

While I started out doing this on my own there have been a few helping hands along the way:

* Daniel Farnand for making invest some more time in the tools and stretching the ideas
* Mike Miller (facebook) for pointing me in the right direction to Walter K. Zydhek's work on the find detail of
  Microsoft Color Basic
* Ciaran Anscomb for maintaining the incredibly useful XROAR emulator
