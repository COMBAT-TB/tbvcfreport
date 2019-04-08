from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='tbvcfreport',
    version='0.0.8',
    url='https://github.com/COMBAT-TB/tbvcfreport',
    bugtrack_url='https://github.com/COMBAT-TB/tbvcfreport/issues',
    description="Parses SnpEff generated VCF and generates an HTML report.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='neo4j,vcf,tb',
    license="GPLv3",
    py_modules=['tbvcfreport'],
    packages=find_packages(),
    package_data={
        'tbvcfreport': ['templates/*.html'],
    },
    install_requires=[
        'click',
        'py2neo',
        'jinja2',
        'tqdm',
        'pyvcf',
        'snpit',
    ],
    dependency_links=[
        'git+https://github.com/samlipworth/snpit.git@V1.1#egg=snpit',
    ],
    entry_points={
        'console_scripts': ['tbvcfreport=tbvcfreport.tbvcfreport:cli']
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Lavnguage :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
