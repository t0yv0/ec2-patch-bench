# Copyright 2022, Pulumi Corporation.  All rights reserved.
#
# (setq fill-column 120)


import pulumi
import pulumi_aws as aws
import pulumi_command as command
import base64


def bench_infra(prefix, size, region, profile,
                key_name, public_key, private_key):
    aws_provider = aws.Provider(f"{prefix}-provider",
                                region=region,
                                profile=profile)

    # Create a new security group that permits SSH access.
    secgrp = aws.ec2.SecurityGroup(f"{prefix}-secgrpallowssh",
        description='allow-port-22-ssh-access',
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                protocol='tcp',
                from_port=22,
                to_port=22,
                cidr_blocks=['0.0.0.0/0']),
        ],
        egress=[aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            cidr_blocks=["0.0.0.0/0"],
            ipv6_cidr_blocks=["::/0"],
        )],
        opts=pulumi.ResourceOptions(provider=aws_provider))

    # Get the AMI
    ami = aws.ec2.get_ami(
        owners=['amazon'],
        most_recent=True,
        filters=[aws.ec2.GetAmiFilterArgs(
            name='name',
            values=['amzn2-ami-hvm-*x86_64*'],
        )],
        opts=pulumi.invoke.InvokeOptions(provider=aws_provider))

    # Maybe generate a KeyPair.
    if key_name is None:
        key = aws.ec2.KeyPair(f"{prefix}-key",
            public_key=public_key,
            opts=pulumi.ResourceOptions(provider=aws_provider)
        )
        key_name = key.key_name

    # Provision a server as an EC2 instance.
    server = aws.ec2.Instance(f"{prefix}-server",
        instance_type=size,
        ami=ami.id,
        key_name=key_name,
        vpc_security_group_ids=[secgrp.id],
        opts=pulumi.ResourceOptions(provider=aws_provider)
    )

    # Configure SSH connector.
    connection = command.remote.ConnectionArgs(
        host=server.public_ip,
        user='ec2-user',
        private_key=private_key
    )

    # Copy a provisionig bundle to the server.
    cp_config = command.remote.CopyFile(f"{prefix}-provisioner-bundle",
        connection=connection,
        local_path='patch-testing.zip',
        remote_path='patch-testing.zip',
        opts=pulumi.ResourceOptions(depends_on=[server])
    )

    # Execute a basic provisioning command on our server.
    provisioner = command.remote.Command(f"{prefix}-provisioner",
        connection=connection,
        create='unzip patch-testing.zip && bash ./patch-testing/provision.sh',
        opts=pulumi.ResourceOptions(depends_on=[cp_config])
    )

    # Copy benchmarking script.
    bench_runner = command.remote.CopyFile(f"{prefix}-bench-runner",
        connection=connection,
        local_path='bench.sh',
        remote_path='bench.sh',
        opts=pulumi.ResourceOptions(depends_on=[server]),
    )

    # Run benchmarks.
    provisioner = command.remote.Command(f"{prefix}-benchmark-runner",
        connection=connection,
        create='bash bench.sh',
        opts=pulumi.ResourceOptions(depends_on=[bench_runner, provisioner])
    )

    return {
        f"{prefix}_public_ip": server.public_ip,
        f"{prefix}_public_host_name": server.public_dns,
    }
