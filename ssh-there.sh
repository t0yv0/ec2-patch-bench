#!/usr/bin/env bash

set -euo pipefail

PREFIX="$1"

HOST=$(pulumi stack output ${PREFIX}_public_host_name)

ssh -i ./rsa ec2-user@$HOST
