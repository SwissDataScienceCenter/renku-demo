# -*- coding: utf-8 -*-
#
# Copyright 2017 - Swiss Data Science Center (SDSC)
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
"""
conftest.py

Package-wide configuration of tests.
Created by Chandrasekhar Ramakrishnan on 2018-01-23.
Copyright (c) 2018 Chandrasekhar Ramakrishnan. All rights reserved.
"""

import os
from os.path import dirname

import pytest


@pytest.fixture(scope="session")
def data_folder_path():
    """Path to the weather_ch data folder"""
    module_path = dirname(__file__)
    data_path = os.path.join(module_path, "..", "..", "..", "..", "data")
    return data_path


@pytest.fixture(scope="session")
def zh_data_file_path():
    """Path to the file with data for Zürich"""
    return os.path.join(data_folder_path(), "homog_mo_SMA.txt")
