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

import requests
import os
import json

gitlab_url = os.environ.get('GITLAB_URL')
gitlab_sudo_token = os.environ.get('GITLAB_SUDO_TOKEN')

headers = {'Accept': 'application/json', 'Private-Token': gitlab_sudo_token}

# Remove our two users and all their contributions
with open('users.json', 'r') as f:
    users = json.load(f)

for user in users:
    response = requests.get(
        gitlab_url + '/api/v4/users',
        params={'username': user['username']},
        headers=headers
    )
    if response.status_code >= 300:
        print('\nProblem getting id for user {0}'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)

    for user in response.json():
        deletion_response = requests.delete(
            gitlab_url + '/api/v4/users/{0}'.format(user['id']),
            params={'hard_delete': True},
            headers=headers
        )
        if deletion_response.status_code >= 300:
            print('\nProblem deleting user {0}'.format(user['username']))
            print(response.text)
            print('Aborting...\n')
            exit(1)
