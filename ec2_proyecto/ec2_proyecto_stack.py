from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class Ec2ProyectoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Usar el VPC por defecto
        vpc = ec2.Vpc.from_lookup(self, "MyDefaultVpc", is_default=True)  # Esto obtiene el VPC por defecto

        # Crear un grupo de seguridad (Security Group)
        security_group = ec2.SecurityGroup(self, "MySecurityGroup",
            vpc=vpc,  # Asociarlo al VPC por defecto
            security_group_name="MyInstanceSecurityGroup"
        )

        # Abrir el puerto 22 para SSH
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),  # Permitir acceso desde cualquier IP
            ec2.Port.tcp(22),  # Puerto 22 (SSH)
            "Allow SSH access from anywhere"
        )

        # Abrir el puerto 80 para HTTP
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),  # Permitir acceso desde cualquier IP
            ec2.Port.tcp(80),  # Puerto 80 (HTTP)
            "Allow HTTP access from anywhere"
        )

        # Crear la instancia EC2 con el grupo de seguridad y volumen de 20 GB
        instance = ec2.CfnInstance(self, "MyInstance",
            instance_type="t2.micro",  # Ajusta el tipo de instancia según sea necesario
            image_id="ami-0363234289a7b6202",  # ID de la AMI de "Cloud9ubuntu22"
            subnet_id=vpc.public_subnets[0].subnet_id,  # Usando la primera subred pública del VPC por defecto
            key_name="vockey",  # Usamos 'vockey' como el par de claves existente
            security_group_ids=[security_group.security_group_id],  # Asignamos el grupo de seguridad creado
            block_device_mappings=[  # Configuración del disco EBS
                ec2.CfnInstance.BlockDeviceMappingProperty(
                    device_name="/dev/xvda",  # Nombre del dispositivo
                    ebs=ec2.CfnInstance.EbsProperty(
                        volume_size=20,  # Tamaño del disco (20 GB)
                        volume_type="gp2"  # Tipo de volumen (General Purpose SSD)
                    )
                )
            ]
        )
