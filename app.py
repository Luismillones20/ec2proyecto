from aws_cdk import App, Environment, DefaultStackSynthesizer
from ec2_proyecto.ec2_proyecto_stack import Ec2ProyectoStack


app = App()

# Configura el entorno con la cuenta y la región de AWS
env = Environment(account="276665510567", region="us-east-1")

synthesizer = DefaultStackSynthesizer(
    qualifier='ec2proj',
    cloud_formation_execution_role='arn:aws:iam::276665510567:role/LabRole'
) 
# Inicializa el stack con el entorno configurado
Ec2ProyectoStack(app, "Ec2ProyectoStack", env=env,synthesizer= synthesizer)

app.synth()
