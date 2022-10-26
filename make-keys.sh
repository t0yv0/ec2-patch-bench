#!/usr/bin/env bash

set -euo pipefail

ssh-keygen -t rsa -f rsa -b 4096 -m PEM
