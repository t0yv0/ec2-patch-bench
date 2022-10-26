# Copyright 2022, Pulumi Corporation.  All rights reserved.
#
# (setq fill-column 120)

from bench_infra import bench_infra
import base64
import keys
import pulumi
import pulumi_aws as aws
import pulumi_command as command
import subprocess as sp

profile = 'devsandbox'
size = 'm6i.large'


configs = [
    {'prefix': 'oregon',   'region': 'us-west-2'},
    {'prefix': 'virginia', 'region': 'us-east-1'},
    {'prefix': 'mumbai',   'region': 'ap-south-1'},
    {'prefix': 'tokyo',    'region': 'ap-northeast-1'},
    {'prefix': 'frankfurt','region': 'eu-central-1'},
]


# Rebuild the provisioning bundle.
sp.check_call('./make-bundle.sh', shell=True)


for cfg in configs:
    outputs = bench_infra(prefix=cfg['prefix'],
                          size=size,
                          region=cfg['region'],
                          profile=profile,
                          key_name=keys.key_name,
                          public_key=keys.public_key,
                          private_key=keys.private_key)
    for k in outputs:
        pulumi.export(k, outputs[k])
