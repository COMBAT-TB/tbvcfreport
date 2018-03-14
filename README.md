# **vcfreport**

A tool to generate an HTML report from SnpEff produced vcf files.

## Usage

```sh
$ git clone https://github.com/COMBAT-TB/vcf-report.git
$ cd vcf-report
$ virtualenv envname
$ source envname/bin/activate
$ pip install -r requirements.txt
$ pip install --editable .
$ vcfreport --help
$ vcfreport generate vcf_direcory/
```

This will generate and open `output.html` on your browser.
