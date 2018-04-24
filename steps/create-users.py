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

# keycloak_url = os.environ.get('KEYCLOAK_URL')

# TODO: For the time being, we add the users to gitlab and not to keycloak for simplicity.
# TODO: Later, the users should be added to Keycloak for to match a realistic setting.

gitlab_url = os.environ.get('GITLAB_URL')
gitlab_sudo_token = os.environ.get('GITLAB_SUDO_TOKEN')

headers = {
    'Accept': 'application/json',
    'Private-Token': gitlab_sudo_token
}


# Create the two users with information stored in the json files
with open('users.json', 'r') as f:
    users = json.load(f)

for user in users:
    response = requests.post(gitlab_url + '/api/v4/users/', data=user, headers=headers)
    if response.status_code == 201:
        user['id'] = response.json()['id']

    # Actually one could recover from this, but I'm too lazy for this now.
    # elif response.status_code == 409:
    #     print('\nProblem on creation of user {0}'.format(user['username']))
    #     print(response.text)
    #     print('Continuing anyway...\n')

    else:
        print('\nProblem on creation of user {0}'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)


# Add the ssh key of the local machine for the first user in the list
with open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r') as pub_key_file:
    key_data = {
        'key': pub_key_file.read(),
        'title': 'my-local-machine'
    }

response = requests.post(gitlab_url + '/api/v4/users/{0}/keys'.format(users[0]['id']), data=key_data, headers=headers)

if response.status_code != 201:
    print('\nProblem adding ssh key for user {0}'.format(users[0]['username']))
    print(response.text)
    print('Aborting...\n')
    exit(1)
