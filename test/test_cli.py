import os

import pytest
from click.testing import CliRunner

from tbvcfreport.tbvcfreport import check_vcf, generate

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_VCF_DIR = os.path.join(CURR_DIR, "test_data/")
TEST_VCF = os.path.join(CURR_DIR, "test_data/test.vcf")
GALAXY_TEST_DATA = os.path.join(os.path.dirname(CURR_DIR), "galaxy/test-data/")


@pytest.fixture(scope="module")
def cli_runner():
    runner = CliRunner()
    return runner


def test_check_vcf():
    """
    Test check_vcf
    :return:
    """
    assert check_vcf(TEST_VCF) is True


# @pytest.mark.skip(reason="no way of currently testing this")
def test_generate(cli_runner):
    result = cli_runner.invoke(generate, [TEST_VCF])
    assert result.exit_code == 0


def test_generate_dr_report(cli_runner):
    result = cli_runner.invoke(
        generate,
        ["--tbprofiler_report",
         os.path.join(GALAXY_TEST_DATA, "rif_resistant.results.json"),
         os.path.join(GALAXY_TEST_DATA, "rif_resistant.vcf")
         ]
    )
    assert result.exit_code == 0
