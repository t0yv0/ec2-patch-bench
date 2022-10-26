#!/usr/bin/env bash

set -euo pipefail

cat rsa.pub | pulumi config set publicKey --
cat rsa | pulumi config set privateKey --secret --
