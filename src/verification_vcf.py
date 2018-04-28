#!/usr/bin/python3
# coding:UTF8

import pandas as pd
import argparse
#import yaml
from io import StringIO



def read_vcf(vcf_filename, columns=None):
    """
    Fonction permettant la lecture du fichier VCF, et Vérification
    du format.

    On parse le fichier VCF, et on récupère les Headers. que l'on va stocker
    dans 3 variables quelconque :
    ==> df
    ==> vcf_header_a
    ==> columns

    Args:
        vcf_reader: a VCFReader object

    Returns:
        df
        vcf_header_a
        columns
    """
    columns = None
    s = StringIO()
    vcf_header_lines = ""

    with open(vcf_filename) as f:
        for line in f:
            if line.startswith('#'):
                if line.startswith('#'):
                    if line.startswith('#CHROM'):
                        columns = line.lstrip("#").split()
                vcf_header_lines += line
            else:
                s.write(line)
    s.seek(0)
    df = pd.read_csv(s, sep="\t",names=columns)
    return df, vcf_header_lines, columns

def check_Vcf_Header(vcf_header_a) :
    """
    Fonction permettant de séparer le contenue du vcf_header en fonction des
    blank_count

    Args:
        str : vcf_header

    Returns:
        list : word_list
    """
    blank_count = vcf_header_a.count(" ")
    deb = 0
    end_offset = vcf_header_a.index(" ")
    word_list = []

    for i in range (0, blank_count + 1):
        word_list.append(vcf_header_a[deb:end_offset])
        vcf_header_a = vcf_header_a[end_offset+1:]
        if (vcf_header_a.count(" ") != 0) :
            end_offset = vcf_header_a.index(" ")
        else :
            end_offset = len(vcf_header_a)
    return word_list

def separation_line(header_vcf):
    """
    Fonction permettant de séparer le contenue du vcf_header en fonction des
    sauts de lignes.
    On récupère ainsi chaque ligne des headers.

    Args:
        str : header_vcf

    Returns:
        list : word_list

    """
    crlf_count = header_vcf.count("\n")
    deb=0
    end_offset = header_vcf.index("\n")
    word_list = []

    for i in range (0, crlf_count + 1) :
        word_list.append(header_vcf[deb:end_offset])
        header_vcf = header_vcf[end_offset+1:]
        if (header_vcf.count ("\n") != 0):
            end_offset =  header_vcf.index("\n")
        else :
            end_offset=len(header_vcf)
    return word_list
