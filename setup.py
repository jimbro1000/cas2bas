import io
import os

from setuptools import setup

CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name='cas2bas',
    version='2.0.0',
    author='Julian Brown',
    author_email='julian@the-lair.info',
    packages=[
        'cas2bas',
        'bas2cas',
        'formats'
    ],
    entry_points={
        'console_scripts': [
            'cas2bas = cas2bas.Main:main',
            'bas2cas = bas2cas.Main:main'
        ]
    },
    url='https://github.com/jimbro1000/cas2bas',
    license='LICENSE',
    description='Quick tool for converting Dragon/Coco CAS format to readable text of basic listing',
    long_description=README,
    install_requires=[
        "pytest",
    ],
)
