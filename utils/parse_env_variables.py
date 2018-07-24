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

import re
import os
import click
from builtins import AttributeError

@click.command()
@click.option('--output', required=True, help='Choose the desired output (\'ssh_port\' or \'host_name\').')
def parse_env_variables(output):
    if output == 'ssh_port':
        try:
            print(re.search(r'\:([0-9]{1,})\/', os.environ['REMOTE_REPO_URL']).group(1))
        except AttributeError:
            print(22)
    elif output == 'host_name':
        print(re.search(r'https?://([^\/]*)', os.environ['GITLAB_URL']).group(1))
    else:
        print('Unknown output option: {}'.format(output))

if __name__ == '__main__':
    parse_env_variables()
