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

with open('users.json', 'r') as f:
    users = json.load(f)

headers = {
    'Accept': 'application/json',
    'Private-Token': gitlab_sudo_token,
    'Sudo': users[0]['username']
}

with open('.gitlab-project-data.json', 'r') as f:
    project_data = json.load(f)

ku3 = {
    'title': 'Analyze Data',
    'description': 'Analyze data to understand weather trends',
}

response = requests.post(
    gitlab_url +
    '/api/v4/projects/{0}/issues'.format(project_data['project']['id']),
    data=ku3,
    headers=headers
)
if response.status_code != 201:
    print('\nProblem creating ku {0}'.format(ku3['title']))
    print(response.text)
    print('Aborting...\n')
    exit(1)
ku3['iid'] = response.json()['iid']

project_data['ku3'] = ku3

# We re-write project and ku information
with open('.gitlab-project-data.json', 'w') as f:
    json.dump(project_data, f)

# Add a contribution to the new ku
ku_url = gitlab_url + \
            '/api/v4/projects/{0}/issues/{1}/notes'.format(project_data['project']['id'], project_data['ku3']['iid'])

note_data = {
    'body':
        'See ![Analysis](notebooks/Analysis.ipynb) for some thoughts on the analysis.'
}

response = requests.post(ku_url, data=note_data, headers=headers)
if response.status_code != 201:
    print('\nProblem adding contribution:', response.text)
    print('Aborting...\n')
    exit(1)
