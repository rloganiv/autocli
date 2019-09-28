from setuptools import find_packages, setup


setup(
    name="autocli",
    version="0.1.1",
    packages=find_packages(exclude=("tests",)),
    install_requires=['numpydoc>=0.9.1']
)
