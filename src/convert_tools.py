#!/usr/bin/python3.5
# coding:UTF8


import argparse
from vcf_model import VcfModel
import sys

"""

 =======================VCF File converter.===========================

"python3.5 nomScript -f methode -a input1.vcf -b input2.vcf -o output.json
--> vcf_filepath, varscan_filepath and output_filepath doivent être fournit.

Args:
    param1: Class VcfModel

Returns:
    JSON Format

Raises:
    KeyError: Raises an exception
"""

def check_arguments() :
    """
    Le module argparse permet l'écriture d'interface de ligne de commande .
    Le programme définit quel arguments est nécéssaire, et Argparse
    comprendra comment analyser ceux hors de sys.argv.
    Module Argparse va générer automatiquement des messages d'aide et d'utilisation
    et émet des erreurs lorsque les utilisateurs donnent des arguments invalides au programme.
    """

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="subparser_dest")

    # ==> Parser pour la méthode variants_to_json ==> Positional argument
    subparser_variants_to_json = subparser.add_parser('variants_to_json', help = 'convert the vcf file to a json file that contains all the variants')
    subparser_variants_to_json.add_argument('-a','--input1', type=str, help = 'Input VCF file name', required = True)
    subparser_variants_to_json.add_argument('-o','--output', type=str, help = 'Output Json file name', required = True)

    # ==> Parser pour la méthode header_to_json ==> Positional argument
    subparser_header_to_json = subparser.add_parser('header_to_json', help = 'convert the vcf file to a json file that contains the  headers ')
    subparser_header_to_json.add_argument('-a','--input1', type=str, help = 'Input VCF file name', required = True)
    subparser_header_to_json.add_argument('-o','--output', type=str, help = 'Output Json file name', required = True)

    # ==> Parser pour la méthode merge_to_json ==> Positional argument
    subparser_merge_to_json = subparser.add_parser('merge_to_json', help = 'Merge the VCF file 1 to the VCF file 2 and produce a json file that contains the variants of this results')
    subparser_merge_to_json.add_argument('-a','--input1', type=str, help = 'Input VCF_1 file name',required=True)
    subparser_merge_to_json.add_argument('-b','--input2', type=str, help = 'Input VCF_2 file name',required=True)
    subparser_merge_to_json.add_argument('-o','--output', type=str, help = 'Output file name', required=True)

    # ==> Parser pour la méthode vcf_to_json ==> Positional ArgumentParser
    subparser_vcf_to_json = subparser.add_parser('vcf_to_json', help = 'convert the vcf file to a json file that contains all the data of this VCF file')
    subparser_vcf_to_json.add_argument('-a','--input1', type=str, help = 'Input VCF file name', required = True)
    subparser_vcf_to_json.add_argument('-o','--output', type=str, help = 'Output Json file name', required = True)

    # ==> Parser pour la méthode retain_all ==> Positional argument
    subparser_retain_all = subparser.add_parser("retain_all', help='modify VCF instance variants keeping only common variants with VCF_2.")
    subparser_retain_all.add_argument('-a','--input1', type=str, help='Input VCF file name', required=True)
    subparser_retain_all.add_argument('-b','--input2', type=str, help='Input VCF_2 file name', required=True)
    subparser_retain_all.add_argument('-o','--output', type=str, help='Output file name', required=True)

    args = parser.parse_args()


    if args.subparser_dest == "variants_to_json":
        variants_to_json(args.input1,args.output)

    elif args.subparser_dest == "header_to_json":
        header_to_json(args.input1, args.output)

    elif args.subparser_dest == "vcf_to_json":
        vcf_to_json(args.input1, args.output)

    elif  args.subparser_dest == "merge_to_json":
        merge_to_json (args.input1,args.input2,args.output)

    elif args.subparser_dest == "retain_all":
        retain_all (args.input1, args.input2, args.output)

    else :
        parser.print_help()
        sys.exit(2)


def variants_to_json (vcf_filepath,json_filepath) :
    v1 = VcfModel(vcf_filepath)
    v1.variants_to_json(json_filepath)


def header_to_json (vcf_filepath,json_filepath) :
    v1 = VcfModel(vcf_filepath)
    v1.header_to_json(header_to_json)

def vcf_to_json (vcf_filepath,json_filepath) :
    v1 = VcfModel(vcf_filepath)
    v1.vcf_to_json(vcf_filepath)

def merge_to_json (vcf1_filepath,vcf2_filepath,json_filepath) :
    v1 = VcfModel(vcf1_filepath)
    v2 = VcfModel(vcf2_filepath)
    VcfModel.merge_to_json(v1, v2, json_filepath)

def retain_all (vcf1_filepath,vcf2_filepath,json_filepath) :
    v1 = VcfModel(vcf1_filepath)
    v2 = VcfModel(vcf2_filepath)
    v2.retain_all(v1)
    v2.variants_to_json(json_filepath)

# ============================> Main <===================================
def main ():
    check_arguments()


if __name__ == "__main__":
    main()
