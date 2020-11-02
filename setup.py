# -*- coding: utf-8 -*-

import ast
import io
import re
import os
from setuptools import find_packages, setup

DEPENDENCIES = []
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="processit",
    version="1.0.0",
    author="Infodevelopers pvt. ltd.",
    author_email="info@infodev.com.np",
    description="This package is dedicated to provide ease to developers to preprocess the textual content",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tatkaal/preprocessor",
    include_package_data=True,
    zip_safe=False,
    test_suite="tests.test_project",
    packages=["processit"],
    python_requires=">=3.4",
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
