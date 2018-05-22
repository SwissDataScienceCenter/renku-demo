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
preprocess.py

Module with functions for preprocessing data.

Created by Chandrasekhar Ramakrishnan on 2018-04-16.
Copyright (c) 2018 Chandrasekhar Ramakrishnan. All rights reserved.
"""

import pandas as pd


def standardize_df(df):
    """Convert a frame of temperatures to deviation from monthly mean"""
    center = df.groupby('Month')[['Temperature', 'Precipitation']].median()

    def standardize(x):
        std = x.assign(
            Temperature=x['Temperature'] - center.loc[x.name, 'Temperature']
        )
        std = std.assign(
            Precipitation=x['Precipitation'] -
            center.loc[x.name, 'Precipitation']
        )
        return std

    return df.groupby('Month').apply(standardize)


def to_standardized(df, out_path):
    """Convert a frame of temperatures to deviation from monthly mean and write the result"""
    dfs = standardize_df(df)
    dfs = dfs.reset_index(0, drop=True).sort_index()
    dfs.to_csv(out_path)
