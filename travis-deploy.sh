#!/bin/env bash
#
# Copyright 2018 - Swiss Data Science Center (SDSC)
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

# Push image to dockerhub
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD ;
if [[ -n $TRAVIS_TAG ]]; then
    docker build . -t renku/renku-demo:${TRAVIS_TAG} --build-arg RENKU_VERSION=v${TRAVIS_TAG}
    docker push renku/renku-demo:${TRAVIS_TAG}
else
    docker push renku/renku-demo ;
fi
