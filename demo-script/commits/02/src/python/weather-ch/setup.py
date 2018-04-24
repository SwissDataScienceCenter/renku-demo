# -*- coding: utf-8 -*-


# Apache Software License 2.0
# 
# Copyright (c) 2018, Swiss Data Science Center (SDSC)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from setuptools import find_packages, setup

install_requires = [req.strip() for req in "numpy, scipy, pandas, jupyter, seaborn, matplotlib, statsmodels".split(',')]

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

setup(
    name="weather_ch",
    version="0.1.0",
    url="https://github.com/SwissDataScienceCenter/weather-ch",

    author="Swiss Data Science Center (SDSC)",
    author_email="contact@datascience.ch",

    description="Umbrella package for weather-ch.",
    long_description=open('README.rst').read(),

    packages=find_packages(),
    zip_safe=True,

    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=['pytest'],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
