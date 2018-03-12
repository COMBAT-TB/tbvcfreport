import os
import webbrowser
import click
from vcfproc import VCFProc
from report import render_report


@click.group()
def cli():
    """
    vcfreport is a command line tool that generates an HTML-based VCF report.
    """
    pass


@cli.command()
@click.argument('vcf_dir', type=click.Path(exists=True))
def generate(vcf_dir):
    """
    Generate report from VCF files in VCF_DIR.
    """
    vcf_file = VCFProc(vcf_dir=vcf_dir)
    snp_list = vcf_file.parse()
    report = render_report(data=snp_list)
    webbrowser.open('file://' + os.path.realpath(report))


if __name__ == '__main__':
    generate()
