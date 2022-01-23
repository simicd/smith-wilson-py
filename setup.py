import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="smithwilson",
    version="0.2.0",
    author="Dejan Simic",
    author_email="dejan.simic",
    description="Implementation of the Smith-Wilson yield curve fitting algorithm in Python for interpolations and extrapolations of zero-coupon bond rates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simicd/smith-wilson-py.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=required,
)
