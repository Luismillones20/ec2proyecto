import aws_cdk as core
import aws_cdk.assertions as assertions

from ec2_proyecto.ec2_proyecto_stack import Ec2ProyectoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ec2_proyecto/ec2_proyecto_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Ec2ProyectoStack(app, "ec2-proyecto")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
