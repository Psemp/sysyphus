from setuptools import setup, find_packages

setup(
    name="sysphus",
    version="0.0.1",
    author="Pierre Sempéré",
    author_email="pierre.sempere.01@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "beautifulsoup4",
        "re",
        "requests",
    ],
    description="""Structured meteorite data access using MetBull: Query, filter, and analyze with ease.""",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Psemp/sysyphus.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
