from setuptools import setup, find_packages

setup(
    name="sysyphus",
    version="0.1.1",
    author="Pierre Sempéré",
    author_email="pierre.sempere.01@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "beautifulsoup4",
        "requests",
        "tqdm",
    ],
    python_requires=">=3.10",
    description="""Structured meteorite data access using MetBull: Query, filter, and analyze with ease.""",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Psemp/sysyphus.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
