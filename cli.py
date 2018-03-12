import click
from vcfparser import VCFParser
from generate import create_report


@click.command()
@click.argument('vcf_dir', type=click.Path(exists=True))
def generate_report(vcf_dir):
    vcf_file = VCFParser(vcf_dir=vcf_dir)
    snp_list = vcf_file.parse()
    create_report(data=snp_list)


if __name__ == '__main__':
    generate_report()
