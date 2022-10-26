#!/usr/bin/env bash

set -euo pipefail

rm -rf patch-testing/patch-testing
rm -rf patch-testing/pulumi-access-token.secret

# (cd patch-testing && env GOOS=linux GOARCH=amd64 go build -o patch-testing)

PULUMI_ACCESS_TOKEN=$(pass pulumi.com/t0yv0/macbook-token)
echo -n $PULUMI_ACCESS_TOKEN > patch-testing/pulumi-access-token.secret

rm -rf patch-testing.zip
zip -r patch-testing.zip patch-testing
