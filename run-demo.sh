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

#export KEYCLOAK_URL=${KEYCLOAK_URL:-http://keycloak.renga.build:8080}
#export KEYCLOAK_ADMIN_USER=${KEYCLOAK_ADMIN_USER:-admin}
#export KEYCLOAK_ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD:-admin}
export GITLAB_URL=${GITLAB_URL:-http://gitlab.renga.build}
export GITLAB_SUDO_TOKEN=${GITLAB_SUDO_TOKEN:-dummy-secret}

echo ==================================
echo Using the following env variables:
#echo Keycloak URL: $KEYCLOAK_URL
#echo Keycloak admin user: $KEYCLOAK_ADMIN_USER
#echo Keycloak admin password: $KEYCLOAK_ADMIN_PASSWORD
echo GitLab URL: $GITLAB_URL
echo GitLab sudo token: $GITLAB_SUDO_TOKEN
echo ==================================


bash steps/check-packages.sh

# If the necessary software is around, we create a new virtualenv, activate it and install the requirements.
virtualenv -p python3 .venv
source ./.venv/bin/activate
echo -n Installing python packages...
pip install -q -r requirements.txt
echo done.

python steps/create-users.py

python steps/create-project.py

# Read the remote repository URL, and username/email of the primary user
# from the json file using python.
export REMOTE_REPO_URL=$(python -c \
    "import json; print(json.load(open('.gitlab-project-data.json'))['project']['ssh_url_to_repo'])")
export PRIMARY_USER_NAME=$(python -c "import json; print(json.load(open('users.json'))[0]['name'])")
export PRIMARY_USER_EMAIL=$(python -c "import json; print(json.load(open('users.json'))[0]['email'])")

bash steps/initialize-repo.sh

bash steps/implement-reader/commit.sh
python steps/implement-reader/ku.py


bash steps/preprocess-data/commit.sh
python steps/preprocess-data/ku.py

bash steps/analyze-data/commit.sh
python steps/analyze-data/ku.py


echo Demo project setup was successful
