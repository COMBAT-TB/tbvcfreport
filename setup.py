from setuptools import setup, find_packages

setup(
    name='tb_vcfreport',
    version='0.0.1',
    url='https://github.com/COMBAT-TB/tb-vcf-report',
    bugtrack_url='https://github.com/COMBAT-TB/tb-vcf-report/issues',
    description='Parses SnpEff generated VCF file and creates an HTML based report with links to Combat TB Explorer.',
    keywords='neo4j,vcf,tb',
    py_modules=['tb_vcfreport'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'py2neo',
        'Jinja2',
        'tqdm',
        'PyVCF',
    ],
    entry_points={
        'console_scripts': ['tb_vcfreport=tb_vcfreport.tb_vcfreport:cli']
    },
)
