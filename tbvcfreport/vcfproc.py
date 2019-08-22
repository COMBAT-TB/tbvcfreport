"""Interface to handle VCF files."""
import vcf
from snpit import snpit
try:
    from .dbconn import query_by_gene_list
except ImportError:
    from dbconn import query_by_gene_list


class VCFProc:
    """Process VCF File."""

    def __init__(self, vcf_file, filter_udi=None):
        """initializer."""
        self.vcf_file = vcf_file
        self.filter_udi = filter_udi

    def find_lineage(self):
        """Find lineage."""
        lineage_parser = snpit(input_file=self.vcf_file)
        (species, lineage, sublineage,
         percent_agreement) = lineage_parser.determine_lineage()
        percent_agreement = round(percent_agreement)

        lineage_dict = {
            'species': species,
            'lineage': lineage,
            'sublineage': sublineage,
            'percent_agreement': percent_agreement
        }

        return lineage_dict

    def parse(self):
        """Parse VCF."""
        variants, rv_tags = [], []
        with open(self.vcf_file) as _vcf:
            vcf_reader = vcf.Reader(_vcf)
            for i, record in enumerate(vcf_reader):
                if record.INFO.get('ANN'):
                    annotations = self.get_variant_ann(record=record)
                    for annotation in annotations:
                        effect = annotation[1]
                        if self.filter_udi and self.filter_variants(effect):
                            continue
                        gene_identifier = annotation[4]
                        rv_tags.append(gene_identifier)
        rv_tags = list(set(rv_tags))
        gene_info = self.gene_info_to_dict(query_by_gene_list(rv_tags))
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
                        effect = annotation[1]
                        if self.filter_udi and self.filter_variants(effect):
                            continue
                        gene_identifier = annotation[4]
                        variant_data = gene_info.get(gene_identifier,
                                                     {'gene': None,
                                                         'protein': None,
                                                         'pathway': None})
                        annotation.extend([
                            record.CHROM, record.POS, record.REF,
                            record.var_type, affected_region,
                            variant_data])
                        variants.append(annotation)
        return variants

    @staticmethod
    def filter_variants(effect):
        """Filter variants."""
        if effect in ('upstream_gene_variant',
                      'downstream_gene_variant',
                      'intergenic_region'):
            return True
        return False

    @staticmethod
    def gene_info_to_dict(gene_info):
        """Gene info to dictionary."""
        # gene_info is a list of dictionaries, with
        # each dictionary having keys 'gene', 'protein' and 'pathway'
        info_dict = {}
        for info in gene_info:
            assert all([key in info for key in ('gene', 'protein', 'pathway')]
                       ), f"missing key in info, keys are {info.keys()}"
            uniquename = info['gene']['uniquename']
            info_dict[uniquename] = info
        return info_dict

    @staticmethod
    def get_variant_ann(record):
        """Get Annotation from ANN."""
        annotations = [ann.split("|") for ann in record.INFO['ANN']]
        return annotations
