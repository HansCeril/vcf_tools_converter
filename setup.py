#!/usr/bin/python3
# coding:UTF8
#---------Library-------------------------#
from setuptools import setup
#-----------------------------------------#

with open ("README1.md", "r") as fileR :
    description_library  = fileR.read()


setup (
    name = "project_Stage_Hans",
    version = "1.0",
    description = "useful VCF tool",
    license='MIT',
    long_description = description_library,
    url = "https://github.com/HansCeril/vcf_tools_converter",
    author_email = "bioinfo@CHRU-LILLE.FR",
    keywords='genetics genome Human variants Allele insertion computational',
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
     ],
    install_requires = ["setuptools","argparse"],
    package_data = {
        '': ['*.vcf', '*.gz', '*.tbi'],
        },



)
