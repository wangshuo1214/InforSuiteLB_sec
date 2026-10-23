import re
from setuptools import setup, find_packages

with open("inforsuitelb_sec/__init__.py") as fd:
    version = re.search(
        r'^version\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

install_requires = [
    'cached-property>=1.2.0;python_version<"3.8"',
    'argparse>=1.4.0;python_version<"3.2"',
    "Jinja2>=2.8",
    "ConfigArgParse>=0.11.0",
]

deep_requires = ["redoctor>=0.1.5"]

tests_requires = [
    "pytest>=7.0.0",
    "pytest-xdist",
]

# README.md is not present in Docker image setup
long_description = None
try:
    with open("README.md", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    pass

setup(
    name="InforSuiteLB_sec",
    version=version,
    description="InforSuiteLB configuration [sec]analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="inforsuitelb security lint static-analysis",
    author="InforSuiteLB",
    author_email="security@inforsuitelb.local",
    url="",
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["inforsuitelb_sec=inforsuitelb_sec.cli.main:main"],
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    extras_require={
        "deep": deep_requires,
        "tests": install_requires + deep_requires + tests_requires,
        "rich": ["rich>=13.0.0"],
    },
)
