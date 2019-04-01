"""
Interface to handle VCF files
"""
from collections import namedtuple
import logging
import sys

import vcf
from tqdm import tqdm

try:
    from .dbconn import get_gene_data, query_by_gene_list
except (ImportError, ValueError):
    from dbconn import get_gene_data, query_by_gene_list

log = logging.getLogger(__name__)


class VCFProc(object):
    """
    Process VCF File
    """
    class LineRecord(object):
        CHROM = POS = REF = var_type = affected_region = variant_data = None
        def __init__(self):
            pass

    class VariantInfo(object):
        gene = protein = pathway = None
    variant_info = namedtuple('variant_info', ['gene',
                              'protein', 'pathway'])
    def __init__(self, vcf_file):
        self.vcf_file = vcf_file

    def parse(self):
        variants, rv_tags = [], []
        if self.vcf_file.endswith(".vcf"):
            log.info("Processing: {}...\n".format(self.vcf_file))
            with open(self.vcf_file) as _vcf:
                vcf_reader = vcf.Reader(_vcf)
                for i, record in enumerate(vcf_reader):
                    if record.INFO.get('ANN'):
                        annotations = self.get_variant_ann(record=record)
                        for annotation in annotations:
                            # TODO: make this kind of filtering optional
                            if annotation[1] in ('upstream_gene_variant', 'downstream_gene_variant', 'intergenic_region'):
                                continue
                            gene_identifier = annotation[4]
                            rv_tags.append(gene_identifier)
            rv_tags = list(set(rv_tags))
            gene_info = self.gene_info_to_dict(query_by_gene_list(list(set(rv_tags))))
            with open(self.vcf_file) as _vcf:
                vcf_reader = vcf.Reader(_vcf)
                for i, record in enumerate(vcf_reader):
                    if record.var_type == 'snp':
                        record.affected_start += 1
                    affected_region = "..".join(
                        [str(record.affected_start), str(record.affected_end)])
                    if record.INFO.get('ANN'):
                        annotations = self.get_variant_ann(record=record)
                        # Usually there is more than one annotation reported in
                        # each ANN. A variant can affect multiple genes
                        for annotation in annotations:
                            # TODO: make this kind of filtering optional
                            if annotation[1] in ('upstream_gene_variant', 'downstream_gene_variant'):
                                continue
                            gene_identifier = annotation[4]
                            variant_data = gene_info.get(gene_identifier,
                                                         {'gene': None,
                                                          'protein': None,
                                                          'pathway': None})
                            annotation.extend([record.CHROM, record.POS, record.REF,
                                               record.var_type, affected_region,
                                               variant_data])
                            variants.append(annotation)
        else:
            sys.stderr.write("Can't parse {vcf_file}".format(
                vcf_file=self.vcf_file))
        return variants

    @staticmethod
    def gene_info_to_dict(gene_info):
        # gene_info is a list of dictionaries, with
        # each dictionary having keys 'gene', 'protein' and 'pathway'
        info_dict = {}
        for info in gene_info:
            assert all([key in info for key in ('gene', 'protein', 'pathway')]), "missing key in info, keys are {}".format(info.keys())
            uniquename = info['gene']['uniquename']
            info_dict[uniquename] = info
        return info_dict

    @staticmethod
    def get_variant_ann(record):
        """
        Get Annotation from ANN
        :param record:
        :return:
        """
        annotations = []
        if record.INFO.get('ANN'):
            annotations = [ann.split("|") for ann in record.INFO['ANN']]
        return annotations
