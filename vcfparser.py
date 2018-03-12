"""
Interface to handle VCF files
"""
import os
import sys
import glob
import vcf


class VCFParser(object):
    def __init__(self, vcf_dir=None):
        self.vcf_dir = vcf_dir

    def parse(self):
        snp_dict = dict()
        snp_list = []
        count = 0
        for vcf_file in glob.glob(self.vcf_dir + "/*.vcf"):
            if vcf_file.endswith(".vcf"):
                sys.stderr.write(
                    "Processing: {}\n".format(os.getcwd()+'/'+vcf_file))
                with open(vcf_file) as _vcf:
                    vcf_reader = vcf.Reader(_vcf)
                    for record in vcf_reader:
                        count = count + 1
                        annotation = self.get_variant_ann(record=record)
                        snp_dict[annotation[4]] = annotation
                        snp_list.append(annotation)
        print(count)
        print(len(snp_dict))
        print(len(snp_list))
        return snp_list

    @staticmethod
    def get_variant_ann(record=None):
        ann = record.INFO['ANN'][0].split('|')
        # print(ann)
        return ann
