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
reader_test.py

Tests for reading.

Created by Chandrasekhar Ramakrishnan on 2018-01-23.
Copyright (c) 2018 Chandrasekhar Ramakrishnan. All rights reserved.
"""

import os

from weather_ch import reader


def test_reader(zh_data_file_path):
    assert os.path.exists(zh_data_file_path)
    df = reader.read_data(zh_data_file_path)
    assert df.loc[0,'Year'] == 1864
    assert df.loc[0,'Month'] == 1
    assert df.loc[0,'Temperature'] == -6.6
    assert df.loc[0,'Precipitation'] == 25.7
