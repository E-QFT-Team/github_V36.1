from setuptools import setup, find_packages

setup(
    name="eqft-v361",
    version="1.0.0",
    author="E-QFT Development Team",
    author_email="eqft.dev@example.com",
    description="Implementation of E-QFT V36.1 for lepton g-2 calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-account/eqft-v361-framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
    ],
)