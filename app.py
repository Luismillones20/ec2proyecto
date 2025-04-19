from aws_cdk import App, Environment
from ec2_proyecto.ec2_proyecto_stack import Ec2ProyectoStack

app = App()

# Configura el entorno con la cuenta y la región de AWS
env = Environment(account="276665510567", region="us-east-1")

# Inicializa el stack con el entorno configurado
Ec2ProyectoStack(app, "Ec2ProyectoStack", env=env)

app.synth()
