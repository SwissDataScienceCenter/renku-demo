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
gitlab_url = os.environ.get('GITLAB_URL')
gitlab_sudo_token = os.environ.get('GITLAB_SUDO_TOKEN')


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
    print(response.status_code)
    exit(1)


# Prepare the headers for keycloak and gitlab

gitlab_headers = {
    'Accept': 'application/json',
    'Private-Token': gitlab_sudo_token
}

keycloak_headers = {
    'Accept': 'application/json',
    'Authorization': 'bearer ' + response.json()['access_token'],
    'Content-Type': 'application/json'
}


# Create the two users with information stored in the json files

with open('users.json', 'r') as f:
    users = json.load(f)

for user in users:
    user['name'] = '{0} {1}'.format(user['firstName'], user['lastName'])

    # Create the user in keycloak

    kc_post_user = {key: user[key] for key in ['firstName', 'lastName', 'username', 'email']}
    kc_post_user['emailVerified'] = True
    kc_post_user['enabled'] = True

    response = requests.post(keycloak_url + '/auth/admin/realms/Renga/users',
                             data=json.dumps(kc_post_user),
                             headers=keycloak_headers)

    if response.status_code != 201:
        print('\nProblem on creation of user {0} in keycloak'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)


    # Get the id of the newly created user.

    # Feels a bit stupid, don't know why keycloak doesn't
    # include it in the response to the POST request...?

    response = requests.get(keycloak_url + '/auth/admin/realms/Renga/users',
                             params={'username': user['username']},
                             headers=keycloak_headers)

    if response.status_code == 200:
        user['keycloak_id'] = response.json()[0]['id']
    else:
        print('\nCan not find user {0} in keycloak'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)


    # Add the password to the user in keycloak

    kc_user_credentials = {
        'type': 'password',
        'temporary': False,
        'value': user['password']
    }

    response = requests.put(keycloak_url + '/auth/admin/realms/Renga/users/{0}/reset-password'.format(user['keycloak_id']),
                             data=json.dumps(kc_user_credentials),
                             headers=keycloak_headers)
    if response.status_code >= 300:
        print('\nCan not add password fo user {0} in keycloak'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)


    # Add the same user to GitLab

    gitlab_post_user = {
        'username': user['username'],
        'email': user['email'],
        'name': user['name'],
        'extern_uid': user['username'],
        'provider': 'oauth2_generic',
        'skip_confirmation': True,
        'reset_password': False,
        'password': user['password']
    }

    response = requests.post(gitlab_url + '/api/v4/users/', data=gitlab_post_user, headers=gitlab_headers)
    if response.status_code == 201:
        user['id'] = response.json()['id']

    # Actually one could recover from this, but I'm too lazy for this now.
    # elif response.status_code == 409:
    #     print('\nProblem on creation of user {0}'.format(user['username']))
    #     print(response.text)
    #     print('Continuing anyway...\n')

    else:
        print('\nProblem on creation of user {0} in GitLab'.format(user['username']))
        print(response.text)
        print('Aborting...\n')
        exit(1)


# Add the ssh key of the local machine for the first user in the list
with open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r') as pub_key_file:
    key_data = {
        'key': pub_key_file.read(),
        'title': 'my-local-machine'
    }

response = requests.post(gitlab_url + '/api/v4/users/{0}/keys'.format(users[0]['id']),
                         data=key_data, headers=gitlab_headers)

if response.status_code != 201:
    print('\nProblem adding ssh key for user {0}'.format(users[0]['username']))
    print(response.text)
    print('Aborting...\n')
    exit(1)
