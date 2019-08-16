"""Interface to CLI."""

import os

import click
from snpit import snpit

try:
    from .report import generate_report
    from .vcfproc import VCFProc
    from .tbprofiler import get_tb_profiler_data
except ImportError:
    from report import generate_report
    from vcfproc import VCFProc
    from tbprofiler import get_tb_profiler_data


def check_vcf(vcf_file):
    """Check vcf file for emptiness.

    :param vcf_file:
    :return:
    """
    _file = False
    file_name = vcf_file.split('/')[-1]
    if not vcf_file.endswith(".vcf"):
        click.secho(f"{file_name} is not a VCF file!\n", fg='red')
    elif os.stat(vcf_file).st_size > 0 and vcf_file.endswith(".vcf"):
        _file = True
    else:
        click.secho(f"{file_name} is empty!\n", fg='red')
    return _file


def find_lineage(vcf_file):
    """Find lineage."""
    lineage_parser = snpit(input_file=vcf_file)
    (species, lineage, sublineage,
     percent_agreement) = lineage_parser.determine_lineage()
    percent_agreement = round(percent_agreement)

    return (species, lineage, sublineage, percent_agreement)


def parse_and_generate_report(vcf_file, tbprofiler_report=None):
    """Parse VCF file and generate report."""
    drug_resistance_list, rrs_variant_count = [], 0
    file_name = vcf_file.split('/')[-1].split('.')[0]
    click.secho(f"Processing {file_name}...\n", fg='green')
    (species, lineage, sublineage,
        percent_agreement) = find_lineage(vcf_file)
    vcf_file = VCFProc(vcf_file=vcf_file)
    variants = vcf_file.parse()
    if tbprofiler_report:
        (drug_resistance_list,
            rrs_variant_count) = get_tb_profiler_data(
            tbprofiler_report, variants)
    generate_report(file_name=file_name, data={
        'variants': variants,
        'lineage': {
            'species': species,
            'lineage': lineage,
            'sublineage': sublineage,
            'percent_agreement': percent_agreement
        },
        'dr_data': drug_resistance_list,
        'mixed_infection': rrs_variant_count > 1})


@click.group()
def cli():
    """Generate an HTML-based VCF report from SnpEff annotated VCF file(s)."""
    pass


@cli.command()
@click.option('-t', '--tbprofiler_report', default=None, show_default=True,
              type=click.File())
@click.argument('vcf_dir', type=click.Path(exists=True))
def generate(vcf_dir, tbprofiler_report):
    """Generate an interactive HTML-based report."""
    if os.path.isdir(vcf_dir):
        for root, dirs, files in os.walk(vcf_dir):
            if len(os.listdir(vcf_dir)) == 0:
                click.secho(f"{vcf_dir} is empty!\n", fg='red')
            for vcf_file in files:
                (base, ext) = os.path.splitext(vcf_file)
                vcf_file = os.path.join(os.path.abspath(vcf_dir), vcf_file)
                if check_vcf(vcf_file):
                    parse_and_generate_report(vcf_file, tbprofiler_report)

    elif os.path.isfile(vcf_dir):
        vcf_file = os.path.abspath(vcf_dir)
        if check_vcf(vcf_file):
            parse_and_generate_report(vcf_file, tbprofiler_report)
    else:
        click.secho(f"Can't generate report for {vcf_dir}!\n", fg='red')


if __name__ == '__main__':
    generate()
