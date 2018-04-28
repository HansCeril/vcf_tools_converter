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

    # CONSTANTE
    CHEMIN_ACCES_VCF = "Example/vcfExample.vcf"
    CHEMIN_ACCES_VARSCAN = "Example/varScanExample.vcf"
    SOURCE = 'source'
    FILEFORMAT = 'fileformat'
    REFERENCE = 'reference'
    NS = 'NS'
    DP = 'DP'
    H2 = 'H2'
    DB = 'DB'
    AF = 'AF'
    WT = 'WT'
    HOM = 'HOM'
    ADP = 'ADP'
    NC = 'NC'


    def test_metadata_function(self):
        """ Test de notre fonction permettant d'extraire les métadatas

        Nous testerons cette fonction pour les fichiers obtenues du variant
        caller ainsi que du Varscan

        Args:
            None

        Returns:
           unittest
        """

        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(fic1vcf.metadata[self.__class__.SOURCE], ['myImputationProgramV3.1'])
        self.assertEqual(fic1vcf.metadata[self.__class__.FILEFORMAT], 'VCFv4.3')
        self.assertEqual(fic1vcf.metadata[self.__class__.REFERENCE],'file:///seq/references/1000GenomesPilot-NCBI36.fasta')

        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(fic1varScan.metadata[self.__class__.SOURCE], ['VarScan2'])
        self.assertEqual(fic1varScan.metadata[self.__class__.FILEFORMAT], 'VCFv4.1')

    def test_info_patientName_function(self) :
        """ Test de notre fonction permettant de récupérer le nom du patient

        Nous testerons cette fonction pour les fichiers Variant caller ainsi que
        les fichiers VarScan

        Args:
            None

        Returns:
           unittest
        """

        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(fic1vcf.patient_name, ['NA00001', 'NA00002', 'NA00003'])

        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(fic1varScan.patient_name,['Sample1'])

    def test_dico_contig_function(self) :
        """ Test de notre fonction permettant d'extraire les contigs
        Nous testerons cette fonction pour les fichiers Variants caller ainsi que
        les fichiers VarScan
        Args:
            None
        Returns:
           unittest
        """
        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(fic1vcf.dico_contig['20'], 62435964)
        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(fic1varScan.dico_contig, {})

    def test_infos_function(self) :
        """ Test de notre fonction permettant d'extraire les infos du fichier VCF
        Nous testerons cette fonction pour les fichiers Variant caller ainsi que
        les fichiers VarScan
        Args:
            None
        Returns:
           unittest
        """
        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(fic1vcf.infos[self.__class__.NS], [1, 'Integer', 'Number of Samples With Data', None, None])
        self.assertEqual(fic1vcf.infos[self.__class__.DP], [1, 'Integer', 'Total Depth', None, None])
        self.assertEqual(fic1vcf.infos[self.__class__.H2], ['.', 'Flag', 'HapMap2 membership', None, None])
        self.assertEqual(fic1vcf.infos[self.__class__.DB], ['.', 'Flag', 'dbSNP membership, build 129', None, None])
        self.assertEqual(fic1vcf.infos[self.__class__.AF], ['A', 'Float', 'Allele Frequency', None, None])

        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(fic1varScan.infos[self.__class__.WT], [1, 'Integer', 'Number of samples called reference (wild-type)', None, None])
        self.assertEqual(fic1varScan.infos[self.__class__.HOM],[1, 'Integer', 'Number of samples called homozygous-variant', None, None])
        self.assertEqual(fic1varScan.infos[self.__class__.ADP],[1, 'Integer', 'Average per-sample depth of bases with Phred score >= 0', None, None])
        self.assertEqual(fic1varScan.infos[self.__class__.NC], [1, 'Integer', 'Number of samples not called', None, None])



    def test_variants_funtions(self) :
        """ Test de notre fonction permettant d'extraire les informations
        des variants de notre fichier VCF
        Nous testerons cette fonction pour les fichiers Variant caller ainsi que
        les fichiers VarScan
        Args:
            None
        Returns:
           unittest
        """
        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(len(fic1vcf.variants), 5)

        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(len(fic1varScan.variants), 253)

    def test_annotated_functions(self):
        """ Test de notre fonction permettant de savoir si notre fichier est
        annoté ou non
        Nous testerons cette fonction pour les fichiers Variant caller ainsi que
        les fichiers VarScan
        Args:
            None
        Returns:
            unittest
        """
        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(fic1vcf.annotated, False)

        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(fic1varScan.annotated, False)

    def test_format_function(self) :
        """ Test de notre fonction permettant de savoir si notre fichier est
        annoté ou non
        Nous testerons cette fonction pour les fichiers Variant caller ainsi que
        les fichiers VarScan
        Args:
            None
        Returns:
            unittest
        """
        fic1vcf = VcfModel(self.__class__.CHEMIN_ACCES_VCF)
        self.assertEqual(len(fic1vcf.format), 4)

        fic1varScan = VcfModel(self.__class__.CHEMIN_ACCES_VARSCAN)
        self.assertEqual(len(fic1varScan.format), 14)


if __name__ == '__main__':
    unittest.main()
