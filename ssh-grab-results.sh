#!/usr/bin/env bash

set -euo pipefail

PREFIX="$1"
HOST=$(pulumi stack output ${PREFIX}_public_host_name)

rsync -a ec2-user@$HOST:./patch-testing/ data/$HOST/
