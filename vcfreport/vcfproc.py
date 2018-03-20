"""
Interface to handle VCF files
"""
import sys
import vcf
from tqdm import tqdm
from dbconn import get_gene_data


class VCFProc(object):
    """
    Process VCF File
    """

    def __init__(self, vcf_file):
        self.vcf_file = vcf_file

    def parse(self):
        snp_list, rv_tags = [], []
        if self.vcf_file.endswith(".vcf"):
            sys.stdout.write(
                "Processing: {}...\n".format(self.vcf_file))
            with open(self.vcf_file) as _vcf:
                vcf_reader = vcf.Reader(_vcf)
                for record in tqdm(vcf_reader):
                    if record.var_type == 'snp':
                        record.affected_start += 1
                    affected_region = "..".join([str(record.affected_start), str(record.affected_end)])
                    annotation = self.get_variant_ann(record=record)
                    gene_identifier = annotation[4]
                    rv_tags.append(gene_identifier)
                    variant_data = self.get_variant_data(
                        gene_identifier)
                    annotation.extend(
                        [record.CHROM, record.POS, record.REF,
                         record.var_type, affected_region, variant_data]
                    )
                    snp_list.append(annotation)
        else:
            sys.stderr.write("Can't parse {vcf_file}".format(
                vcf_file=self.vcf_file))
        return snp_list

    @staticmethod
    def get_variant_ann(record):
        """
        Get Annotation from ANN
        :param record:
        :return:
        """
        ann = record.INFO['ANN'][0].split('|')
        return ann

    @staticmethod
    def get_variant_data(entry):
        """
        Get variant data from DB
        :param entry:
        :return:
        """
        data = get_gene_data(entry)
        return data
