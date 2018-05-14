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

headers = {
    'Accept': 'application/json',
    'Private-Token': gitlab_sudo_token,
}

with open('users.json', 'r') as f:
    users = json.load(f)

# Create the weather-zh project as primary user, star it, add secondary user as developer
headers['Sudo'] = users[0]['username']

project_data = {
    'name': 'weather-zh',
    'description': 'An investigation into weather trends in Zürich, Switzerland.',
    'visibility': 'public',
    'tag_list': 'linear models, python, weather',
}

response = requests.post(gitlab_url + '/api/v4/projects/', data=project_data, headers=headers)

if response.status_code == 201:
    project_data['id'] = response.json()['id']
    project_data['ssh_url_to_repo'] = response.json()['ssh_url_to_repo']
else:
    print('\nProblem creating project weather-zh')
    print(response.text)
    print('Aborting...\n')
    exit(1)


requests.post(gitlab_url + '/api/v4/projects/{0}/star'.format(project_data['id']), headers=headers)

# Get id of secondary user
response = requests.get(
    gitlab_url + '/api/v4/users/',
    headers=headers,
    params={'username': users[1]['username']}
)
project_member = {
    'user_id': response.json()[0]['id'],
    'access_level': 30,
}

response = requests.post(
    gitlab_url + '/api/v4/projects/{0}/members'.format(project_data['id']),
    data=project_member,
    headers=headers
)

if response.status_code != 201:
    print('\nProblem adding secondary user as developer')
    print(response.text)
    print('Aborting...\n')
    exit(1)


# Create two kus as secondary user
headers['Sudo'] = users[1]['username']

ku1 = {
    'title': 'Data Reader',
    'description': 'Implement code to read the data',
}

ku2 = {
    'title': 'Preprocess Data',
    'description': 'Convert values to deviation from monthly mean',
}

for ku in [ku1, ku2]:
    response = requests.post(
        gitlab_url + '/api/v4/projects/{0}/issues'.format(project_data['id']),
        data=ku,
        headers=headers
    )
    if response.status_code != 201:
        print('\nProblem creating ku {0}'.format(ku['title']))
        print(response.text)
        print('Aborting...\n')
        exit(1)
    ku['iid'] = response.json()['iid']

# We write project and ku ids to a json file so that some steps can easily be run individually.
with open('.gitlab-project-data.json', 'w') as f:
    json.dump({
        'project': project_data,
        'ku1': ku1,
        'ku2': ku2,
    }, f)

