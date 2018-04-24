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

mkdir weather-zh
renga init weather-zh
cd weather-zh

git commit --amend --no-edit --author="$PRIMARY_USER_NAME <$PRIMARY_USER_EMAIL>"

git config user.email $PRIMARY_USER_EMAIL
git config user.name "$PRIMARY_USER_NAME"

curl https://www.gitignore.io/api/macos,python,R,linux >> .gitignore
git commit -am "Updated gitignore using gitignore.io"

renga dataset create zh
renga dataset add zh http://www.meteoschweiz.admin.ch/product/output/climate-data/homogenous-monthly-data-processing/data/homog_mo_SMA.txt

cp ../demo-script/commits/01/README.md ./
git add .
git commit -m "Added readme"

git remote add origin $REMOTE_REPO_URL
git push --set-upstream origin master
