# **tbvcfreport**

A tool to generate an HTML report from SnpEff produced vcf files with links to the
Combat TB Explorer database.

![VCFReport](./img/tbvcfreport.png)

## Usage

```sh
$ git clone https://github.com/COMBAT-TB/tbvcfreport.git
$ cd tbvcfreport
$ virtualenv envname
$ source envname/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ tbvcfreport --help
$ tbvcfreport generate vcf_direcory/
```

This will generate a `{vcf-file-name}.html` file in `pwd`.
