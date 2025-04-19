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
            "us-east-1": "ami-0363234289a7b6202"  # Reemplaza con la ID real de la AMI de "Cloud9ubuntu22"
        })

        # ARN del rol existente (LabRole)
        role_arn = "arn:aws:iam::276665510567:role/LabRole"

        # Crear la instancia EC2 con el rol existente usando CfnInstance
        instance = ec2.CfnInstance(self, "MyInstance",
            instance_type="t2.micro",  # Ajusta el tipo de instancia según sea necesario
            image_id=ami.get_image(self).image_id,  # Obtén la ID de la imagen AMI
            subnet_id=vpc.public_subnets[0].subnet_id,  # Usando la primera subred pública del VPC
            key_name="vockey",  # Usamos 'vockey' como el par de claves existente
            iam_instance_profile=role_arn,  # Asigna el ARN del rol existente
            security_group_ids=[],  # Agrega grupos de seguridad si es necesario
        )

