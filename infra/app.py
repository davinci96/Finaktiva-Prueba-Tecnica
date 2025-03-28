import json
import os
import aws_cdk as core
from cdk_nag import AwsSolutionsChecks
from modules.ecr_stack import EcrStack
from modules.ecs_stack import EcsStack
from modules.alb_stack import AlbStack
from modules.vpc_stack import VpcStack

account = os.getenv("ACCOUNT")

env = core.Environment(account=account, region="us-east-1")


app = core.App()
Aspects.of(app).add(AwsSolutionsChecks(verbose=True))

ecr_stack = EcrStack(app, "EcrStack")

vpc_stack = VpcStack(app, "VpcStack", env=env)

ecs_stack = EcsStack(app, "EcsStack",
    vpc=vpc_stack.vpc,
    ecr_repository1=ecr_stack.ecr_repository,
    env=env
)

alb_stack = AlbStack(app, "AlbStack",
    vpc=vpc_stack.vpc,
    ecs_service1=ecs_stack.service1,
    env=env
)

cloudwatch_stack = CloudWatchStack(app, "CloudWatchStack",
    ecs_services=ecs_stack.services,
    env=env
)


app.synth()

