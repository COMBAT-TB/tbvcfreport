from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tbvcfreport",
    version="0.1.8",
    url="https://github.com/COMBAT-TB/tbvcfreport",
    author="SANBI",
    author_email="help@sanbi.ac.za",
    description="Parses SnpEff annotated M.tb VCF(s) and generates an interactive HTML-based report.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="neo4j,vcf,tuberculosis,h37rv,snpeff",
    license="GPLv3",
    py_modules=["tbvcfreport"],
    packages=find_packages(),
    package_data={
        "tbvcfreport": ["templates/*.html"],
    },
    python_requires=">=3.8",
    install_requires=[
        "click",
        "neo4j",
        "jinja2",
        "pyvcf",
    ],
    entry_points={"console_scripts": ["tbvcfreport=tbvcfreport.tbvcfreport:cli"]},
    project_urls={
        "Project": "https://combattb.org",
        "Source": "https://github.com/COMBAT-TB/tbvcfreport",
        "Tracker": "https://github.com/COMBAT-TB/tbvcfreport/issues",
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
