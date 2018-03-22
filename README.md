# **tb_vcfreport**

A tool to generate an HTML report from SnpEff produced vcf files with links to the 
Combat TB Explorer database.

## Usage

```sh
$ git clone https://github.com/COMBAT-TB/tb-vcf-report.git
$ cd tb-vcf-report
$ virtualenv envname
$ source envname/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ tb_vcfreport --help
$ tb_vcfreport generate vcf_direcory/
```

This will generate a `{vcf-file-name}.html` file in `pwd`.
