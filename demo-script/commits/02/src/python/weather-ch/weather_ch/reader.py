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
reader.py

Module with functions for reading data.

Created by Chandrasekhar Ramakrishnan on 2018-01-22.
Copyright (c) 2018 Chandrasekhar Ramakrishnan. All rights reserved.
"""

import pandas as pd


def read_data(path_to_data):
    """Read data and return a pandas data frame."""
    return pd.read_table(path_to_data, sep="\s+", skip_blank_lines=False, header=27)
