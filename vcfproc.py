"""
Interface to handle VCF files
"""
import os
import sys
import glob
import vcf


class VCFProc(object):
    def __init__(self, vcf_dir=None):
        self.vcf_dir = vcf_dir

    def parse(self):
        snp_list = []
        for vcf_file in glob.glob(self.vcf_dir + "/*.vcf"):
            file_name = vcf_file.split('/')[-1].split('.')[0]
            if vcf_file.endswith(".vcf"):
                sys.stdout.write(
                    "Processing: {}\n".format(os.getcwd() + '/' + vcf_file))
                with open(vcf_file) as _vcf:
                    vcf_reader = vcf.Reader(_vcf)
                    for record in vcf_reader:
                        annotation = self.get_variant_ann(record=record)
                        annotation.extend(
                            [record.CHROM, record.POS, record.REF,
                                record.var_type, file_name]
                        )
                        snp_list.append(annotation)
        return snp_list

    @staticmethod
    def get_variant_ann(record=None):
        ann = record.INFO['ANN'][0].split('|')
        return ann
