"""Interface to CLI."""

import os

import click

try:
    from .report import generate_report
    from .vcfproc import VCFProc
    from .tbprofiler import TBProfilerReport
except ImportError:
    from report import generate_report
    from vcfproc import VCFProc
    from tbprofiler import TBProfilerReport


def check_vcf(vcf_file):
    """Check vcf file for emptiness.

    :param vcf_file:
    :return:
    """
    base_name = os.path.basename(vcf_file)
    (name, ext) = os.path.splitext(base_name)
    if os.stat(vcf_file).st_size > 0 and ext == ".vcf":
        return True
    else:
        if ext != ".vcf":
            raise TypeError(f"Expected a VCF file. Found {base_name}!")
        else:
            raise OSError(f"VCF file: {base_name} is empty!")
    return False


def parse_and_generate_report(vcf_file, filter_udi, json_report=None):
    """Parse VCF file and generate report."""
    drug_resistance_list, rrs_variant_count = [], 0
    vcf_base_name = os.path.basename(vcf_file)
    (vcf_file_name, ext) = os.path.splitext(vcf_base_name)
    click.secho(f"Processing {vcf_base_name}...\n", fg='green')

    vcf_proc = VCFProc(vcf_file=vcf_file, filter_udi=filter_udi)
    lineage = vcf_proc.find_lineage()
    variants = vcf_proc.parse()

    if json_report:
        json_base_name = os.path.basename(
            os.path.abspath(json_report.name))
        (_, ext) = os.path.splitext(json_base_name)
        if ext != ".json":
            raise TypeError(f"Expected a json file. Found {json_base_name}!")

        tbprofiler = TBProfilerReport(json_report, variants)
        (drug_resistance_list, rrs_variant_count) = tbprofiler.get_data()

    data = {
        'variants': variants,
        'lineage': lineage,
        'dr_data': drug_resistance_list,
        'mixed_infection': rrs_variant_count > 1
    }

    generate_report(file_name=vcf_file_name, data=data)


@click.group()
def cli():
    """Generate an HTML-based VCF report from SnpEff annotated VCF(s)."""
    pass


@cli.command()
@click.option('-t', '--tbprofiler-report', default=None, type=click.File(),
              help="TBProfiler json report.")
@click.option('-f/-nf', '--filter-udi/--no-filter-udi', default=True,
              show_default=True,
              help="Filter upstream, downstream and intergenic variants.")
@click.argument('vcf_dir', type=click.Path(exists=True), required=True)
def generate(vcf_dir, tbprofiler_report, filter_udi):
    """Generate an interactive HTML-based VCF report."""
    if os.path.isdir(vcf_dir):
        for root, dirs, files in os.walk(vcf_dir):
            if len(os.listdir(vcf_dir)) == 0:
                raise OSError(f"Directory: {vcf_dir} is empty!")
            for vcf_file in files:
                vcf_file = os.path.join(os.path.abspath(vcf_dir), vcf_file)
                if check_vcf(vcf_file):
                    # TODO: support generating DR reports for "directory mode"
                    parse_and_generate_report(vcf_file, filter_udi)
    elif os.path.isfile(vcf_dir):
        vcf_file = os.path.abspath(vcf_dir)
        if check_vcf(vcf_file):
            parse_and_generate_report(vcf_file, filter_udi, tbprofiler_report)
    else:
        click.secho(f"Can't generate report for {vcf_dir}!\n", fg='red')


if __name__ == '__main__':
    generate()
