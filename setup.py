

from setuptools import find_packages
from setuptools import setup

from biomarkers import read_version_txt

setup(
    name="biomarkers",
    version=read_version_txt(),
    packages=find_packages(),
    install_requires=[
        "click>=8.0.1",
        "pydantic>=1.8.2",
        "pandas>=1.1.0",
        "pytest>=6.0.1",
        "clingo>=5.5.0.post3",
        "pyboolnet @ git+https://github.com/hklarner/pyboolnet"
    ],
    entry_points="""
        [console_scripts]
        biomarkers=biomarkers.cli.main:main
    """,
    package_data={"": ["version.txt"]},
    include_package_data=True,
)


