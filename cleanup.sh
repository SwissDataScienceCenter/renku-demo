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
    source ./.venv/bin/activate
fi

# Remove the users and the remote repo
python steps/cleanup-gitlab.py
python steps/cleanup-keycloak.py

# Remove the local repo
rm -rf ./weather-zh
rm ./.gitlab-project-data.json

# Remove traces of the virtual environment
if [ -z "$DOCKER" ]; then
    deactivate
    rm -rf ./.venv
fi

if ! [ -z "$DOCKER" ]; then
    # Finally remove the known_hosts
    rm ~/.ssh/known_hosts
fi

echo Demo project was cleaned up successfully
