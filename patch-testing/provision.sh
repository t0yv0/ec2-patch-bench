#!/usr/bin/env bash

set -euo pipefail

stack="bench-$RANDOM"
rc=16
rp=1024

echo "== installing pulumi ==============================================="
curl -fsSL https://get.pulumi.com | sh
export PATH=~/.pulumi/bin:$PATH
echo "== installed pulumi $(pulumi version) =============================="

echo "== installing golang ==============================================="
sudo yum install golang -y
echo "== installed golang %(go version) =================================="

echo "== go mod tidy ====================================================="
(cd patch-testing && go mod tidy)
echo "== done go mod tidy ================================================"

echo "== go build . ======================================================"
(cd patch-testing && go build .)
echo "== done go build . ================================================="

echo "== configure pulumi stack =========================================="
export PULUMI_ACCESS_TOKEN=$(cat patch-testing/pulumi-access-token.secret)
(cd patch-testing && pulumi stack init $stack)
(cd patch-testing && pulumi stack select $stack)
(cd patch-testing && pulumi config set \
                            patch-testing:resource_count $rc)
(cd patch-testing && pulumi config set \
                            patch-testing:resource_payload_bytes $rp)
echo "== done configure pulumi stack ====================================="

echo "== pulumi preview =================================================="
(cd patch-testing && pulumi preview)
echo "== done pulumi preview ============================================="
