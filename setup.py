from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
exec(open("letra/version.py").read(), version)

setup(
    name="letra",
    version=version["__version__"],
    license="MIT",
    author="Swellaby",
    author_email="opensource@swellaby.com",
    description="Utility for managing GitHub issue labels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swellaby/letra",
    packages=find_packages(),
)
