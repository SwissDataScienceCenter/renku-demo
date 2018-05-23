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

export KEYCLOAK_URL=${KEYCLOAK_URL:-http://keycloak.renku.build:8080}
export KEYCLOAK_ADMIN_USER=${KEYCLOAK_ADMIN_USER:-admin}
export KEYCLOAK_ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD:-admin}
export GITLAB_URL=${GITLAB_URL:-http://gitlab.renku.build}
export GITLAB_SUDO_TOKEN=${GITLAB_SUDO_TOKEN:-dummy-secret}

echo ==================================
echo Using the following env variables:
echo Keycloak URL: $KEYCLOAK_URL
echo Keycloak admin user: $KEYCLOAK_ADMIN_USER
echo Keycloak admin password: $KEYCLOAK_ADMIN_PASSWORD
echo GitLab URL: $GITLAB_URL
echo GitLab sudo token: $GITLAB_SUDO_TOKEN
echo ==================================

if [ -z "$DOCKER" ]; then
    bash steps/1-check-packages.sh

    # If the necessary software is around, we create a new virtualenv, activate it and install the requirements.
    virtualenv -p python3 .venv
    source ./.venv/bin/activate
    echo -n Installing python packages...
    pip install -q -r requirements.txt
    echo done.
fi



if ! [ -z "$DOCKER" ]; then
    mkdir .ssh
    ssh-keygen -t rsa -N "" -b 4096 -f ~/.ssh/id_rsa
fi

python steps/2-create-users.py

python steps/3-create-project.py

# Read the remote repository URL, and username/email of the primary user
# from the json file using python.
export REMOTE_REPO_URL=$(python -c \
    "import json; print(json.load(open('.gitlab-project-data.json'))['project']['ssh_url_to_repo'])")
export PRIMARY_USER_NAME=$(python -c "
import json;
user = json.load(open('users.json'))[0];
print('{0} {1}'.format(user['firstName'], user['lastName']))
")
export PRIMARY_USER_EMAIL=$(python -c "import json; print(json.load(open('users.json'))[0]['email'])")

bash steps/4-initialize-repo.sh

bash steps/implement-reader/5-commit.sh
python steps/implement-reader/6-ku.py


bash steps/preprocess-data/7-commit.sh
python steps/preprocess-data/8-ku.py

bash steps/analyze-data/9-commit.sh
python steps/analyze-data/10-ku.py


echo Demo project setup was successful
