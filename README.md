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

### Run demo inside docker container
**The recommended way** to run the demo script is to use the prepared docker image:
- `docker run --rm --network host renku/renku-demo` runs the script.
- `docker run --rm --network host renku/renku-demo /app/cleanup.sh` removes the demo project 
from your gitlab instance.
If you want to build your image locally (for example because you want to change the pre-configured
users in users.json), run `docker build . -t renku/renku-demo`
