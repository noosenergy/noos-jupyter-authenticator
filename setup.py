#!/usr/bin/env python
# -*- coding: utf-8 -*

from setuptools import find_packages, setup


VERSION = "0.1"

REQUIREMENTS = [
    "jupyterhub>=0.8",
    "tornado",
    "traitlets",
]


setup_args = dict(
    # Description
    name="neptune-jupyter-auth",
    version=VERSION,
    # Credentials
    url="https://github.com/noosenergy/neptune-jupyter-auth",
    license="Proprietary",
    # Package data
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["*tests*"]),
    # Dependencies
    install_requires=REQUIREMENTS,
)


if __name__ == "__main__":

    # Make install
    setup(**setup_args)
