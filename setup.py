import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dicey",
    version="0.1.0",
    author="Chase Franklin",
    author_email="gnullbyte@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnullbyte/dicey",
    packages=setuptools.find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=["lark-parser"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
