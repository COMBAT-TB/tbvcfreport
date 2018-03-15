"""
Interface to handle VCF files
"""
import os
import sys
import vcf
from tqdm import tqdm
from dbconn import get_gene_data


class VCFProc(object):
    def __init__(self, vcf_dir):
        self.vcf_dir = vcf_dir

    def parse(self):
        snp_list = []
        rv_tags = []
        for root, dirs, files in os.walk(self.vcf_dir):
            for vcf_file in files:
                if vcf_file.endswith(".vcf"):
                    vcf_file_abspath = '/'.join(
                        [os.path.abspath(self.vcf_dir), vcf_file]
                    )
                    file_name = vcf_file.split('.')[0]
                    sys.stdout.write("Processing: {}...\n".format(vcf_file))
                    with open(vcf_file_abspath) as _vcf:
                        vcf_reader = vcf.Reader(_vcf)
                        for record in tqdm(vcf_reader):
                            annotation = self.get_variant_ann(record=record)
                            gene_identifier = annotation[4]
                            rv_tags.append(gene_identifier)
                            variant_data = self.get_variant_data(
                                gene_identifier)
                            annotation.extend(
                                [record.CHROM, record.POS, record.REF,
                                    record.var_type, file_name, variant_data]
                            )
                            snp_list.append(annotation)
        return snp_list

    @staticmethod
    def get_variant_ann(record):
        ann = record.INFO['ANN'][0].split('|')
        return ann

    @staticmethod
    def get_variant_data(entry):
        data = get_gene_data(entry)
        return data
