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
    name="jupyterauth-neptune",
    version=VERSION,
    # Credentials
    url="https://github.com/noosenergy/jupyterauth-neptune",
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
