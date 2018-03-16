"""
Interface to handle VCF files
"""
import sys
import vcf
from tqdm import tqdm
from dbconn import get_gene_data


class VCFProc(object):
    def __init__(self, vcf_file):
        self.vcf_file = vcf_file

    def parse(self):
        snp_list, rv_tags = [], []
        if self.vcf_file.endswith(".vcf"):
            sys.stdout.write(
                "Processing: {}...\n".format(self.vcf_file))
            file_name = self.vcf_file.split('/')[-1].split('.')[0]
            with open(self.vcf_file) as _vcf:
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
        else:
            sys.stderr.write("Can't parse {vcf_file}".format(
                vcf_file=self.vcf_file))
        return snp_list

    @staticmethod
    def get_variant_ann(record):
        ann = record.INFO['ANN'][0].split('|')
        return ann

    @staticmethod
    def get_variant_data(entry):
        data = get_gene_data(entry)
        return data
