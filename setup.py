from setuptools import setup, find_packages

setup(
    name='tbvcfreport',
    version='0.0.3',
    url='https://github.com/COMBAT-TB/tbvcfreport',
    bugtrack_url='https://github.com/COMBAT-TB/tbvcfreport/issues',
    description='Parses SnpEff generated VCF file and creates an HTML based report with links to Combat TB Explorer.',
    keywords='neo4j,vcf,tb',
    license="MIT",
    py_modules=['tbvcfreport'],
    packages=find_packages(),
    package_data={
        'tbvcfreport': ['templates/*.html'],
    },
    install_requires=[
        'click',
        'py2neo',
        'Jinja2',
        'tqdm',
        'PyVCF',
    ],
    entry_points={
        'console_scripts': ['tbvcfreport=tbvcfreport.tbvcfreport:cli']
    },
)
