import io
import os
from setuptools import find_packages, setup

CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name='cas2bas',
    version='0.1.0',
    author='Julian Brown',
    # author_email='',
    packages=['cas2bas'],
    scripts=[],
    entry_points={
        'console_scripts': [
            'cas2bas = cas2bas.cas2bas:main',
        ]
    },
    # url='',
    # license='LICENSE.txt',
    description='Quick tool for converting Dragon/Coco CAS format to readable text of basic listing',
    long_description=README,
    install_requires=[
        "pytest",
    ],
)
