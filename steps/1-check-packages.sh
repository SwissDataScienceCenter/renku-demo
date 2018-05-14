#!/usr/bin/env bash

# -*- coding: utf-8 -*-
#
# Copyright 2017-2018 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

echo 'Checking if necessary software packages are installed...'

# Check if python 3 exists
python3 --version > /dev/null 2>&1
if [ $? = 0 ]
then
    echo python 3 is installed
else
    echo please install python 3
    exit 1
fi


# Check if we have virtualenv
virtualenv --version > /dev/null 2>&1
if [ $? = 0 ]
then
    echo virtualenv is installed
else
    echo please install virtualenv
    exit 1
fi


# Check if git exists
git --version > /dev/null 2>&1
if [ $? = 0 ]
then
    echo git is installed
else
    echo please install git
    exit 1
fi

exit 0
