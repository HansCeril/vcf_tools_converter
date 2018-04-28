#!/usr/bin/python3
# coding:UTF8

#------------------------------library---------------------------------#
import sys
sys.path.append("../src") # or: sys.path.insert(0, os.getcwd())
from vcf_model import VcfModel
import os
import unittest
import json
#--------------------------------------------------------------------#


class TestFuction_VcfModel(unittest.TestCase):
    """ python3 -m unittest test_function_vcfModel.py """

    #CONSTANTE
    VCF_PATH = "Example/vcfExample.vcf"
    JSON_File_PATH = "Example/vcfExample_JSON.json"
    JSON_FILE = JSON_File_PATH


    def create_json (self):
        v1 = VcfModel(self.__class__.VCF_PATH)
        v1.variants_to_json(self.__class__.JSON_File_PATH)

    def read_json(self) :
        data_vcf = open (self.__class__.JSON_FILE).read()
        self.assertEqual(json.loads(data_vcf), True)


if __name__ == '__main__':
    unittest.main()
