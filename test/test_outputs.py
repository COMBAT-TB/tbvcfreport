from test_cli import OUT_TXT_FILE, OUT_HTML_FILE


def test_output():
    assert 'p.Ile245Thr' in open(OUT_TXT_FILE).read()
    assert 'p.Ile245Thr' in open(OUT_HTML_FILE).read()
