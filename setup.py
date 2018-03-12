from setuptools import setup, find_packages

setup(
    name='vcfreport',
    version='0.0.1',
    description='Parses SnpEff generated VCF file and creates an HTML based report.',
    keywords='neo4j,and vcf',
    py_modules=['vcfreport'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'py2neo',
        'tqdm',
        'PyVCF',
    ],
    entry_points={
        'console_scripts': ['vcfreport=vcfreport:cli']
    },
)
