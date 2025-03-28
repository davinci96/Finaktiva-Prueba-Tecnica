import json
import os
from aws_cdk import Stack
from aws_cdk import aws_ecr as ecr
from constructs import Construct
from aws_cdk import RemovalPolicy

class EcrStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        ecr_repository = os.getenv("ECR_REPOSITORY")
        # ecr_repository = "prueba-finaktiva"

        self.ecr_repository = ecr.Repository(self, "MyEcrRepository",
            repository_name=ecr_repository,
            removal_policy=RemovalPolicy.DESTROY
        )

        self.ecr_repository.add_lifecycle_rule(
            tag_prefix_list=["latest"],
            max_image_count=1
        )