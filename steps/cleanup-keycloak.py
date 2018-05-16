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

keycloak_url = os.environ.get('KEYCLOAK_URL')
keycloak_admin_user = os.environ.get('KEYCLOAK_ADMIN_USER')
keycloak_admin_password = os.environ.get('KEYCLOAK_ADMIN_PASSWORD')

# Get an access token with admin power for keycloak. Note that the token
# is only valid for 60 seconds - enough for us!

data = {
    'client_id': 'admin-cli',
    'username': keycloak_admin_user,
    'password': keycloak_admin_password,
    'grant_type': 'password'
}
response = requests.post(keycloak_url + '/auth/realms/master/protocol/openid-connect/token',
                         data=data,
                         headers={'Accept': 'application/json'})
if response.status_code >= 300:
    print('\nProblem obtaining an admin access token for keycloak.')
    exit(1)

keycloak_headers = {
    'Accept': 'application/json',
    'Authorization': 'bearer ' + response.json()['access_token'],
    'Content-Type': 'application/json'
}


# Remove our two users and all their contributions
with open('users.json', 'r') as f:
    users = json.load(f)

for user in users:

    # Get the id(s) of the user(s) with the given username.
    response = requests.get(keycloak_url + '/auth/admin/realms/Renku/users',
                             params={'username': user['username']},
                             headers=keycloak_headers)

    if response.status_code == 200:
        ids = [user['id'] for user in response.json()]
    else:
        print('\nCan not find user {0} in keycloak'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)

    for id in ids:
        response = requests.delete(keycloak_url + '/auth/admin/realms/Renku/users/{0}'.format(id),
                                   headers=keycloak_headers)

        if response.status_code >= 300:
            print('\nProblem deleting user {0} from keycloak with id {1}'.format(user['username'], id))
            print(response.text)
            print('Aborting...\n')
            exit(1)
