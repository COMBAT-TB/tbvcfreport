import os

import pytest
from click.testing import CliRunner

from tbvcfreport.tbvcfreport import check_vcf, generate

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURR_DIR, "test_data/")
TEST_VCF = os.path.join(TEST_DATA_DIR, "test.vcf")
EMPTY_VCF = os.path.join(TEST_DATA_DIR, "empty.vcf")
GALAXY_TEST_DATA = os.path.join(os.path.dirname(CURR_DIR), "galaxy/test-data/")
OUT_DIR = os.path.dirname(CURR_DIR)
OUT_TXT_FILE = os.path.join(OUT_DIR, "test_variants_report.txt")
OUT_HTML_FILE = os.path.join(OUT_DIR, "test_variants_report.html")


@pytest.fixture(scope="module")
def cli_runner():
    runner = CliRunner()
    return runner


def test_check_vcf():
    """Test check_vcf."""
    assert check_vcf(TEST_VCF) is True


# @pytest.mark.skip(reason="no way of currently testing this")
def test_generate_variant_report(cli_runner):
    result = cli_runner.invoke(generate, [TEST_VCF])
    assert result.exit_code == 0


def test_generate_on_empty_vcf(cli_runner):
    result = cli_runner.invoke(generate, [EMPTY_VCF])
    assert result.exit_code == 1
    assert isinstance(result.exception, OSError) is True


def test_generate_on_none_vcf(cli_runner):
    result = cli_runner.invoke(generate, [OUT_TXT_FILE])
    assert result.exit_code == 1
    assert isinstance(result.exception, TypeError) is True


def test_generate_on_none_vcf_exception():
    with pytest.raises(TypeError):
        check_vcf(OUT_TXT_FILE)


def test_generate_on_empty_vcf_exception():
    with pytest.raises(OSError):
        check_vcf(EMPTY_VCF)


def test_generate_dr_report(cli_runner):
    result = cli_runner.invoke(
        generate,
        ["--tbprofiler-report",
         os.path.join(GALAXY_TEST_DATA, "rif_resistant.results.json"),
         os.path.join(GALAXY_TEST_DATA, "rif_resistant.vcf")
         ]
    )
    assert result.exit_code == 0


def test_output():
    assert 'p.Ile245Thr' in open(OUT_TXT_FILE).read()
    assert 'p.Ile245Thr' in open(OUT_HTML_FILE).read()
