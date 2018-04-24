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

set -e

cd weather-zh
cp ../demo-script/commits/03/notebooks/PreprocessData.ipynb ./notebooks/
rm -r src
cp -r ../demo-script/commits/03/src ./
git add -A src/
git add ./notebooks/PreprocessData.ipynb
git commit -m "Work on Ku Preprocess Data"
pip install -e src/python/weather-ch
renga run python -m weather_ch preprocess data/zh/homog_mo_SMA.txt data/zh/standardized.csv
git push
