import pytest

from tbvcfreport.vcfproc import VCFProc
from test_cli import TEST_VCF


@pytest.fixture(scope="module")
def vcf_proc():
    db_url = "bolt://neodb.sanbi.ac.za:7687"
    vcf = VCFProc(vcf_file=TEST_VCF, db_url=db_url)
    return vcf


# @pytest.mark.skip(reason="no way of currently testing this")
def test_parse(vcf_proc):
    result = vcf_proc.parse()
    assert isinstance(result, list) is True
