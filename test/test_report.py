import pytest

from tbvcfreport.report import generate_report


def test_generate_report_exception():
    with pytest.raises(Exception):
        generate_report(file_name=None, data=None)
