import setuptools
import os

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()


with open(os.path.join("network_file_system", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")


setuptools.setup(
    name="network_file_system",
    version=version,
    description="Safe copy, move, and write on remote drives",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/network_file_system",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=[
        "network_file_system",
    ],
    package_data={"network_file_system": []},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
