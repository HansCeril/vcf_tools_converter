# vcf_tools_converter

### A Python library for extracting, manipulating meta-informations of VCF files, tranforming data into Json format

#### Author: Hans CERIL

#### License: MIT

# overview

The Variant Call Format (VCF) is a text file format that contains meta-information
lines, a header line, and each data lines contain information about a position
in the genome.  The format also has the ability to contain genotype information on
samples for each position. It intended to concisely describe reference-indexed variations
between individuals.

Vcf_tools_converter provides in the first way, methods to manipulate meta-informations and sequence variation
as it can be described by VCF. And in the second hand, manipulate the meta-information between two Vcf files provided
by two different algorithm.

This tools is both:
-   an API for extract meta-informations and genomics variants as it can be described by the VCF format
-   a collection of usefull command-line utilities to facilitate the work of the scientist

The API itself provides a quick and extremely permissive method to read and work on vcf file and write into Json file.

## download and install

1. Under the repository name, click to copy the clone URL for the repository. ![](https://help.github.com/assets/images/help/repository/clone-repo-clone-url-button.png)

2. Clone your project : Go to your cumputer's shell and type the following command: `git clone < Paste HTTPS OR SSH Here > `

2. Go to the location where you want the cloned directory to be made:  `cd <PathWhereIWantToClone_vcf_tools_converter>`

3. To easily install Python packages : `sudo python setup.py install`

## development

Two prinicpal file :
-   The file src/vcf_model.py describe methods available in the API
-   the file src/convert_tools describe methods to convert into json format

# Running the tests

Two files test :
-   test/test_fichier_vcf.py :
    -    Tests to verify the format of the vcf file and the varScan file    
-   test/test_function_vcfModel.py :
    -   Tests of the differents methods of our computer tool

Go to the location where the test file are located : `python3.5 -m unittest <test_file.py> `

# executable

### Create object

    usage :
        >>> from vcf_model import VcfModel
        >>>file1 = VcfModel ("FilePathName.vcf")

### variants_to_json


    usage:
        >>> file1.variants_to_json(FilePath)
Extract patient namen and the variants information to store them into a Json file

### header_to_json

    usage :
        >>> file1.header_to_json(FilePath)

Extract header information to store them into a Json file

### vcf_to_json

    usage :
        >>> file1.vcf_to_json(FilePath)

Convert the Vcf file into a Json format


### merge_to_json
    usage :
        >>> file1 = VcfModel("FilePath.vcf")
        >>> file2 = VcfModel("FilePath.vcf.varScan")
        >>> VcfModel.merge_to_json(file1, file2, json_filepath)

Method that merge data of the file2 into the file1 if the data from the file2
are similar to the file1.
This method allowed us to provide additional information.

### retain_all
    usage :
        >>> file2.retain_all (self, file1)
        >>> file2.variants_to_json(FilePath)

An instance function to modify variants of the current Vcf instance by keeping
only the variants common to the given vcf_1.

# Convert format executable

    python3.5 convert_tools.py -f methode -a input1.vcf -b input2.vcf -o output.json

Command line able to convert Vcf files into a Json format.
The user will have the choice of using 4 differents method in this command line :

-   variants_to_json
-   header_to_json
-   vcf_to_json
-   merge_to_json
-   retain_all

Put one or two files you want to work on and write the output json format path way.

A help and usage messages will be send automatically if the users give an invalid arguments
to command line
