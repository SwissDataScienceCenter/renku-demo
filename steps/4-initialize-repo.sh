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

# If we're inside a container we set the git username and email before
# initiating the project to avoid warnings.
if ! [ -z "$DOCKER" ]; then
    git config --global user.email $PRIMARY_USER_EMAIL
    git config --global user.name "$PRIMARY_USER_NAME"
fi

mkdir weather-zh
renku init weather-zh
cd weather-zh

git commit --amend --no-edit --author="$PRIMARY_USER_NAME <$PRIMARY_USER_EMAIL>"

if [ -z "$DOCKER" ]; then
    git config user.email $PRIMARY_USER_EMAIL
    git config user.name "$PRIMARY_USER_NAME"
fi

curl https://www.gitignore.io/api/macos,python,R,linux >> .gitignore
git commit -am "Updated gitignore using gitignore.io"

renku dataset create zh
renku dataset add zh http://www.meteoschweiz.admin.ch/product/output/climate-data/homogenous-monthly-data-processing/data/homog_mo_SMA.txt

cp ../demo-script/commits/01/README.md ./
git add .
git commit -m "Added readme"

if ! [ -z "$DOCKER" ]; then
    export GITLAB_PORT=$(python ../utils/parse_env_variables.py --output ssh_port)
    export GITLAB_HOST=$(python ../utils/parse_env_variables.py --output host_name)

    ssh-keyscan -p $GITLAB_PORT $GITLAB_HOST >> ~/.ssh/known_hosts
fi

git remote add origin $REMOTE_REPO_URL
git push --set-upstream origin master
