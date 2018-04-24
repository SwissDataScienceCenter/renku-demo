# Renga demo

This repo includes instructions to create a repeatable demo of the renga
platform. The steps you need to execute to set up the live demo are described
in [script.md](demo-script/script.md). The actual material for the demo is found in the
`commits` subdirectory.

## Automated setup
All steps up to `Analyze Data` described in the [script.md](demo-script/script.md) are 
automated. Simply run the `run-demo.sh` command. The command assumes a local instance of 
GitLab running under `gitlab.renga.build`, yet it is configurable to run with different 
instances of GitLab as a backend through environment variables. The script `cleanup.sh`
will remove everything created by the `run-demo.sh` script, both locally as well as 
on the GitLab backend.
