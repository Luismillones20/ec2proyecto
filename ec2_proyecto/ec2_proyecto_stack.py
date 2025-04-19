from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class Ec2ProyectoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Crear un VPC (Virtual Private Cloud) para la instancia EC2
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)  # Puedes cambiar el número de zonas de disponibilidad según lo necesites

        # Definir la AMI de Cloud9Ubuntu22 (reemplazar con la ID de la AMI correcta)
        ami = ec2.MachineImage.generic_linux({
            "us-west-2": "ami-0363234289a7b6202"  # Reemplaza con la ID real de la AMI de "Cloud9ubuntu22"
        })

        # Crear el rol de IAM para la instancia EC2 (puede ser una política básica para EC2)
        role = iam.Role(self, "MyInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ReadOnlyAccess")]
        )

        # Crear la instancia EC2 con los parámetros especificados
        instance = ec2.Instance(self, "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),  # Ajusta el tipo de instancia según sea necesario
            machine_image=ami,
            vpc=vpc,
            key_pair=ec2.KeyPair.from_key_pair_name(self, "KeyPair", "vockey"),  # Usamos 'from_key_pair_name' en lugar de 'from_key_name'
            role=role,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20)  # 20 GB de disco
                )
            ]
        )

        # Configuración de los puertos abiertos
        instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22),  # Puerto 22 para SSH
            "Allow SSH access from anywhere"
        )
        instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),  # Puerto 80 para HTTP
            "Allow HTTP access from anywhere"
        )
