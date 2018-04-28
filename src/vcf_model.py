#!/usr/bin/python3
# coding:UTF8

#----library-----#
import os.path
import os
import sys
import vcf
import json
import time
import copy
import errno
import  verification_vcf
#---------------#




class VcfModel(object):

    # CONTANTE
    SAMPLE_NAME = "SAMPLE_NAME"
    CONTIGS = "CONTIGS"
    FORMAT = "FORMAT"
    INFORMATION = "INFORMATIONS"
    METADATA = "METADATA"
    ANNOTATION = "ANNOTATION_?"
    VARIANTS = "VARIANTS"
    CHROM = "CHROM"
    POS = "POS"
    ID = "ID"
    REF = "REF"
    ALT = "ALT"
    QUAL = "QUAL"
    FILTER = "FILTER"
    INFO = "INFO"

    def __init__(self, vcf_file: str) -> None:
        """--Constructeur de notre Object---"""


        #--------------------------------------------------------------------->

        # Vérification du bon format fichier VCF afin de voir s'il est valide
        vcf_a, vcf_header_a, vcf_columns_a = verification_vcf.read_vcf(vcf_file)

        vcf_columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'DATA']
        for col in vcf_columns:
            if col not in vcf_columns_a:
                    vcf_a[col] = "."

        list_header =  verification_vcf.check_Vcf_Header(vcf_header_a)
        list_tab_validation = ["##fileformat", "##fileDate", "##source", "##reference", "##contig"]
        list_header2 =  verification_vcf.separation_line(list_header[0])

        dict_validation = {}
        dict_non_validation = {}

        for j in range (len(list_header2)) :
            for k in range (len(list_tab_validation)):
                if (list_header2[j].startswith(list_tab_validation[k])):
                    dict_validation[list_tab_validation[k]]= "Ok"
                else :
                    dict_non_validation[list_tab_validation[k]] = "Pas Ok"
        if len(dict_validation) >= 2 :
            output_vcf = open(vcf_file)
            self.vcf_reader = vcf.Reader(output_vcf)

        else :
            print ("Erreur de format de fichier : ",dict_non_validation,  dict_validation)


        #-------------------------------------------------------------------->
        self.vcf_reader
        self.metadata = dict
        self.info = dict
        self.format = dict
        self.patient_name = str
        self.dico_contig = dict
        self.infos  = dict
        self.variants  = dict
        self.annotated = bool
        self.source = "source"

        # ---------Methode d'objet--------------------------------

        self._extract_metadata()
        self._variant_information()
        self._extract_contig()
        self._found_patient()
        self._extract_info()
        self._extract_format()
        self._is_annotated()
        output_vcf.close()

    def _extract_contig(self):
        """ method permettant l'extraction des CONTIGs
        Parcours le dictionnaire des contigs du VCF, chaque clef étant le
        nom du contig. Chaque valeur de ce dictionnaire est un tuple qui
        contient de nouveau le nom du contig et sa taille. On extrait la
        clef du dictionnaire et la seconde position du tuple pour en faire
        un nouveau dictionnaire qui contient en clef, le nom du contig et
        en valeur sa taille.

        Args:
            self.vcf_reader: a VCFReader object

        Returns:
            void
        """

        try :
            contig = {}
            for i in self.vcf_reader.contigs:
                contig[i] = self.vcf_reader.contigs[i][1]
            self.dico_contig = contig
            # print (self.dico_contig)
        except IOError as e:
            print (e.errno)


    def _extract_info(self) :
        """ method permettant l'extraction des INFOS du fichier VCF

            Les headers représentant les fichiers VCF,sont représentés de la
            manière sivante :
            ##INFO=<ID=ID,Number=number,Type=type,Description=”description”>

            Parcours le dictionnaire des INFO du VCF, chaque clef étant le
            l'identifiant de l'information. Chaque valeur de ce dictionnaire est
            une liste  qui contient le Number,Type,Description. On extrait la clef du
            dictionnaire et la valeur qui contient les informations complémentaire.
            Certaines valeurs de Number ont été convertie  : "-1" --> A et "0"
            --> ".". Lors de l'utilisation du module PyVCF, ils nous a ainsi donc
            fallut rectifier ces erreurs.

        Args:
            self.vcf_reader: a VCFReader object

        Return:
            void
        """

        try :
            dict_field_info = {}
            for key in self.vcf_reader.infos:
                dict_field_info[key] = list(self.vcf_reader.infos[key][1:])

        except IOError as e:
            print (e.errno)


        try :
            for value in dict_field_info.values():
                if value[0] == -1 :
                    value[0] = 'A'
                elif value[0] == 0 :
                    value[0] = '.'
            self.infos = dict_field_info
            # print (self.infos)
        except Exception as e:
            print (e.message, e.args)


    def _is_annotated (self) :

        """ method permettant de determiner si le fichier est annoté ou pas !

        Parcours des lignes de variants et vérification si ces variants ont
        été annoté par un logiciel quelconque.
        Si l'onglet "CSQ" est présent dans la ligne du variant, dans ce cas
        le fichier est annoté, dans le cas contraire, le fichier n'est pas annoté.

        Args:
            self.vcf_reader: a VCFReader object

        PARAMS output:
           - Void
           """

        try :
            dico_select_info = {}
            for record in self.vcf_reader:

                for inf in record.INFO:
                    dico_select_info[inf] = record.INFO[inf]
        except Exception as e :
            print (e.message, e.args)


        try :
            key_list = []
            arg = 'CSQ'
            for key_info in dico_select_info.keys() :
                key_list.append(key_info)
            if arg not in key_list :
                self.annotated = False
            else :
                self.annotated = True

            # print (self.annotated)
        except Exception as e :
            print (e.message, e.args)


    def _found_patient (self) :
        """ method permettant de récupérer le nom du patient

            A partir du module PyVcf, utilisation d'une méthode d'objet pour
            récupérer les noms du samples.

        Args:
            self.vcf_reader: a VCFReader object

        PARAMS output:
           - Void
        """

        try :
            self.patient_name = self.vcf_reader.samples

        except Exception as e :
            print (e.message, e.args)


    def _extract_metadata(self):
        """ method permettant l'extraction des Metadata du fichier VCF

        Les Metadatas sont les lignes du fichier VCF possédant les
        informations descriptives de l'échantillon.
        Parcours du dictionnaire des META du VCF, chaque clef étant le
        l'identifiant de l'information. Chaque valeur de ce dictionnaire est
        un string qui contient informations de cette clé. On extrait la clef
        du dictionnaire et le string de chaque clé qui contient l'information

        Args:
            self.vcf_reader: a VCFReader object

        PARAMS output:
           - Void
        """

        try :
            self.metadata = {}
            meta = self.vcf_reader.metadata
            for i in meta :
                self.metadata[i]= meta[i]
            # print(self.metadata)
        except Exception as e:
            print (e.message, e.args)


    def _extract_format(self):
        """ method permettant l'extraction de l'header "FORMAT" du fichier VCF

        Format ==> liste extensible (facultatif) des champs pour décrire les
        échantillons.
        On va parcourir le dictionnaire "FORMAT" du vcf, chaque clef étant le
        l'identifiant de l'information. Chaque valeur de ce dictionnaire est
        un string qui contient informations de cette clé. On extrait la clef
        du dictionnaire et string de chaque clé qui contient l'information.

        Args:
            self.vcf_reader: a VCFReader object

        PARAMS output:
           - Void
        """

        try :
            self.format = {}
            form = self.vcf_reader.formats
            for i in form :
                self.format[i] = form[i]
            #print (self.format)
        except Exception as e:
            print (e.message, e.args)


    def _variant_information (self):
        """ method permettant l'extraction des INFORMATIONS du fichier VCF.

        [CHR_POS_REF_ALT] : {"SOURCE" : {"CHROM" : "chr1", "POS" : 10,
        "REF" : ...., "ALT" : (...,...), "INFO" : ....., "FORMAT" : '0/1',1/1}}

        Dans un premier temps, on a creé pour chaque variant une liste contenant
        le chromosome, position, référence, alternative.
        Cette method va retourner un dictionnaire principale contenant cette
        liste. En valeur de chaqu'une de ces variants, nous aurons un dictionnaire
        avec en clé la liste et en valeurs les différentes informations de ces
        variants. (voir exemple ci_dessus)

        Args:
                self.vcf_reader: a VCFReader object

        Return :
                Void
        """

        dico_total3 = {}
        dico_actual_variant = {}
        source_name = str(tuple(self.metadata[self.source]))
        #Erreur ici a cooriger
        for record in self.vcf_reader :
            # alt_list = []
            # print(str(record.ALT[0]))
            # for alt in record.ALT :
            #     alt_list.append(str(alt))
            # tupleKey = tuple (alt_list)

            record_ALT = [str(i) for i in record.ALT]

            name_key = record.CHROM+"_"+str(record.POS)+"_"+record.REF+"_"+"-".join(record_ALT)
            name_key_str = str(name_key)

            dico_total = {}
            dico_total2 ={}

            dico_total[self.__class__.CHROM]=record.CHROM
            dico_total[self.__class__.POS]=record.POS
            dico_total[self.__class__.ID]=record.ID
            dico_total[self.__class__.REF]=record.REF
            dico_total[self.__class__.ALT]=record_ALT
            dico_total[self.__class__.QUAL]=record.QUAL
            dico_total[self.__class__.FILTER]=record.FILTER
            dico_total[self.__class__.INFO]=record.INFO



            dico_sample = {}
            # ------> On va spliter ex => GT:AD:GQ:PL
            s=record.samples[0]
            for f in range (len(record.FORMAT.split(":"))) :
                dico_sample[record.FORMAT.split(":")[f]] = str(s.data[f])
            #print (dico_sample)

            dico_total["FORMAT"]=dico_sample
            dico_total2[source_name] = dico_total
            dico_total3[name_key_str] = dico_total2

        self.variants = dico_total3
        #print (self.variants)


    def variants_to_json(self, json_filepath) :
        """ method permettant l'obtention d'un fichier Json

        Dans ce fichier Json, nous aurons le nom du patient ainsi que tous
        les variants de celui-ci.

        Args:
            json_filepath: a str object for the json filepath. The corresponding
            file will be created.

        PARAMS output:
           - void
        """

        dico_json_variants = {}
        dico_json_variants[self.__class__.SAMPLE_NAME] = self.patient_name
        dico_json_variants[self.__class__.VARIANTS] = self.variants
        print (type(self.variants))
        print (type(dico_json_variants))

        try :
            with open(json_filepath,"w") as json_file:
                json_file.write(json.dumps(dico_json_variants))
                json_file.close()
        except IOError as e:
            print (e.errno)

    def header_to_json(self, json_filepath):
        """ method permettant l'obtention d'un fichier Json

        Dans ce fichier Json contenant uniquement les headers, nous aurons ainsi:
            -> le nom des patients
            -> les CONTIGS
            -> les formats
            -> les infos
            -> les metadatas
            -> bool si le fichier est annoté ou pas

        Args:
            json_filepath: a str object for the json filepath. The corresponding
            file will be created.

        PARAMS output:
           - void
        """

        dico_json_header = {}
        dico_json_header[self.__class__.SAMPLE_NAME] = self.patient_name
        dico_json_header[self.__class__.CONTIGS] = self.dico_contig
        dico_json_header[self.__class__.FORMAT] = self.format
        dico_json_header[self.__class__.INFORMATION] = self.infos
        dico_json_header[self.__class__.METADATA] = self.metadata
        dico_json_header[self.__class__.ANNOTATION] = self.annotated


        try :

            with open(json_filepath, "w") as json_file :
                json_file.write(json.dumps(dico_json_header))

                json_file.close()
        except IOError as e :
            print (e.errno)


    def vcf_to_json (self, json_filepath):
        """ method permettant l'obtention d'un fichier Json

        Dans ce fichier nous aurons les headers ainsi que les variants dans
        notre fichier Json.

        Args:
            json_filepath: a str object for the json filepath. The corresponding
            file will be created.

        Return :
            void
        """

        dico_json_dictionary = {}

        dico_json_dictionary[self.__class__.SAMPLE_NAME] = self.patient_name
        dico_json_dictionary[self.__class__.CONTIGS] = self.dico_contig
        dico_json_dictionary[self.__class__.FORMAT] = self.format
        dico_json_dictionary[self.__class__.INFORMATION] = self.infos
        dico_json_dictionary[self.__class__.METADATA] = self.metadata
        dico_json_dictionary[self.__class__.ANNOTATION] = self.annotated
        dico_json_dictionary[self.__class__.VARIANTS] = self.variants


        try :
            with open( str(json_filepath),"w") as json_file:
                json_file.write(json.dumps(dico_json_dictionary))
                json_file.close()
        except IOError as e:
            print (e.errno)


    @classmethod
    def merge_to_json(cls, vcf_1, vcf_2, json_filepath) :
        """ method permettant de merger les variants du vcf_1 et du
        vcf_2 et de produire un fichier Json.

        [CHR_POS_REF_ALT] : {"VarCaller" : {"CHROM" : "chr1", "POS" : 10,
        "REF" : ...., "ALT" : (...,...), "INFO" : ....., "FORMAT" : '0/1',1/1}
        {"VarScan" : [None]}}
        A partir de ce dictionnaire, nous allons vérifier si la clé du dictionnaire
        de vcf_1 est similaire à la clé de vcf_2. Si c'est le cas, nous
        allons ainsi récupérer les valeurs du dictionnaire "variants" des
        2 objets vcf_1 et vcf_2.
        Dans le cas ou la clé du dictionnaire de vcf_1 est différente
        de celle de vcf_2, on récupère la valeure de vcf_1 et pas celle
        de vcf_2 (None)

        Args:
            vcf_1: instance de VCF
            vcf_2: instance de VCF
            json_filepath: a str object for the json filepath. The corresponding
            file will be created.

        Return :
            void
        """
        try :
            dico_merge_variant_caller = {}
            for key_caller, value_caller in vcf_1.variants.items():
                #print(key_caller)
                dico_merge_variant_caller[key_caller]={**vcf_1.variants.get(key_caller),**vcf_2.variants.get(key_caller,{str(vcf_2.metadata[self.source]): None})}

            with open(str(json_filepath),"w") as json_file:
                json_file.write(json.dumps(dico_merge_variant_caller))
                json_file.close()

        except IOError as e:
            print (e.errno)
            json_file.close()

    def retain_all (self, vcf_1) :
        """ method d'instance permettant de modifier les variants de l'instance
        Vcf actuelle en ne gardant que les variants communs avec le vcf_1 donné
        en paramêtre.

        [CHR_POS_REF_ALT] : {"SOURCE" : {"CHROM" : "chr1", "POS" : 10,
        "REF" : ...., "ALT" : (...,...), "INFO" : ....., "FORMAT" : '0/1',1/1}}
        Nous allons recupérer les variants qui sont identique a ceux
        du vcf_1.

        Pour cela nous allons parcourir la liste de variants la plus petite entre
        celle de l'instance de Vcf actuelle et celle du paramêtre et sélectionner
        uniquement les variants communs.

        Args:
            vcf_1: instance de Vcf

        Return :
            Void

        """

        keys_a = set(vcf_1.variants.keys())
        keys_b = set(vcf_1.variants.keys())


        final_variant = {}
        source_dict={}
        dest_dict={}
        if len(self.variants.keys()) > len(vcf_1.variants.keys()) :
            source_dict = vcf_1.variants.keys()
            dest_dict = self.variants
        else :
            source_dict = self.variants.keys()
            dest_dict = vcf_1.variants

        for key in source_dict :
            if dest_dict.get(key) != None :
                final_variant[key] = self.variants[key]
        self.variants = final_variant
