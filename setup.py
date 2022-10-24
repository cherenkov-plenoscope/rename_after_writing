import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="network_file_system_sebastian-achim-mueller",
    version="0.0.1",
    description="Safe copy, move, and write on remote drives",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/network_file_system",
    project_urls={
        "Bug Tracker": "https://github.com/cherenkov-plenoscope/network_file_system/issues",
    },
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=["network_file_system",],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
