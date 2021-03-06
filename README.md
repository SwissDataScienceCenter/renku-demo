**DEPRECATION NOTICE: This project is outdated an unmaintained. Please check out the [Renku first steps tutorial](https://renku.readthedocs.io/en/latest/tutorials/01_firststeps.html) for a step-by-step guide on how to manually create a meaningful Renku project. For testing existing deployments check out the current version of the [Renku acceptance tests](https://github.com/SwissDataScienceCenter/renku/tree/master/tests).**

# Renku demo

This repo includes instructions to create a repeatable demo of the renku
platform. The steps you need to execute to set up the live demo are described
in [script.md](demo-script/script.md). The actual material for the demo is found in the
`commits` subdirectory.

## Automated setup
All steps up to `Analyze Data` described in the [script.md](demo-script/script.md) are 
automated. Simply run the `run-demo.sh` command. The command assumes a local instance of 
GitLab running under `gitlab.renku.build`, yet it is configurable to run with different 
instances of GitLab as a backend through environment variables. The script `cleanup.sh`
will remove everything created by the `run-demo.sh` script, both locally as well as 
on the GitLab backend. The details (username, password) of the created users can be found 
and adapted in `users.json`.

### Running the demo inside a docker container
**The recommended way** to run the demo script is to use the prepared docker image:
- `docker run --rm --network host renku/renku-demo` runs the script.
- `docker run --rm --network host renku/renku-demo /app/cleanup.sh` removes the demo project 
from your gitlab instance.
If you want to build your image locally (for example because you want to change the pre-configured
users in users.json), run `docker build . -t renku/renku-demo`

### Running the demo against any renku instance
Examples:
- Running the demo against a local minikube deployment: <br>
   `docker run -it --rm --network host \`<br> 
   `-e GITLAB_URL=http://$(minikube ip)/gitlab \`<br> 
   `-e KEYCLOAK_URL=http://$(minikube ip)  \`<br> 
   `renku/renku-demo:latest`

- Running the demo against a cloud deployment of renku: <br>
   `docker run -it --rm --network host \`<br> 
   `-e GITLAB_URL=https://<some-hostname>/gitlab \`<br> 
   `-e KEYCLOAK_URL=https://<some-hostname.  \`<br> 
   `-e KEYCLOAK_ADMIN_USER=admin \`<br> 
   `-e KEYCLOAK_ADMIN_PASSWORD=<get-from-values.yaml> \`<br> 
   `-e GITLAB_SUDO_TOKEN=<get-from-values.yaml>  \`<br> 
   `renku/renku-demo:latest`
   
### Running the demo as kubernetes pod
Examples:
- Running the demo against a local minikube deoployment: <br>
  `kubectl run renku-demo -it \`<br> 
  `--env="GITLAB_URL=http://$(minikube ip)/gitlab" \`<br> 
  `--env="KEYCLOAK_URL=http://$(minikube ip)"  \`<br> 
  `--image=renku/renku-demo:latest  \`<br> 
  `--restart=Never;`<br>
  `kubectl delete pod renku-demo`

- Cleaning up the demo on a local minikube deoployment: <br>
  `kubectl run renku-demo -it \`<br> 
  `--env="GITLAB_URL=http://$(minikube ip)/gitlab" \`<br> 
  `--env="KEYCLOAK_URL=http://$(minikube ip)"  \`<br> 
  `--image=renku/renku-demo:latest  \`<br> 
  `--restart=Never \`<br> 
  `-- /app/cleanup.sh;`<br> 
  `kubectl delete pod renku-demo`
