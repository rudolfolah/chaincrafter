from setuptools import setup, find_packages

setup(
    name="chaincrafter",
    version="0.2.2",
    description="Seamless integration and composability for large language model apps.",
    long_description="Seamless integration and composability for large language model apps.",
    author="Rudolf Olah",
    author_email="rudolf.olah.to@gmail.com",
    url="https://github.com/rudolfolah/chaincrafter",
    packages=find_packages(),
    requires=[
        "pandas==2.0.3",
        "pyyaml==6.0.1",
    ],
    provides=["chaincrafter"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Other/Nonlisted Topic",
    ],
)
