#!/usr/bin/env bash

set -euo pipefail


PREFIX="$1"
FILE="$2"

HOST=$(pulumi stack output ${PREFIX}_public_host_name)

rsync -a "$FILE" "ec2-user@$HOST:./$FILE"
