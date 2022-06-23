#!/bin/bash
# this is meant to be used by github actions.
# takes the full github repository name as argument eg. update_files.sh NebraLtd/hnt_rak-v1
set -eou pipefail

# extract variant and repo directory
repo_name=$1
repo_dir=$(echo ${repo_name} | cut -d '/' -f 2)
variant_name=$(echo ${repo_dir} | cut -d '_' -f 2)

# update docker-compose
cd /home/runner/work/${repo_dir}/${repo_dir}
rm -f docker-compose.yml
wget "https://raw.githubusercontent.com/NebraLtd/helium-miner-software/master/device-compose-files/docker-compose-${variant_name}.yml" -O docker-compose.yml
