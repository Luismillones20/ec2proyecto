from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class Ec2ProyectoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Buscar la VPC predeterminada una sola vez
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # Security Group para puertos 22 y 80
        sg = ec2.SecurityGroup(
            self, "SG",
            vpc=vpc,  # Usamos la VPC aquí
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )

        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        # AMI personalizada
        ami_id = "ami-0363234289a7b6202"  # Reemplaza con la AMI de Cloud9ubuntu22

        # Rol IAM
        iam_role = iam.Role.from_role_arn(self, "LabRole", "arn:aws:iam::276665510567:role/LabRole")

        # Crear la instancia EC2 con un rol IAM
        instancia = ec2.Instance(
            self, "InstanciaEC2",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({"us-west-2": ami_id}),
            vpc=vpc,  # Usamos la VPC aquí
            key_name="vockey",
            security_group=sg,
            role=iam_role,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )]
        )
