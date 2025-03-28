import os
from aws_cdk import Stack, RemovalPolicy
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_logs as logs
from constructs import Construct


class EcsStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, ecr_repository1: ecr.Repository, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ecs_name = os.getenv("ECS_NAME")

        # ecs_name = "prueba-finaktiva"

        self.cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc, cluster_name=ecs_name)

        log_group = logs.LogGroup(self, "LogGroup",
            log_group_name="ecs-logs2",
            removal_policy=RemovalPolicy.DESTROY
        )

        containers = [
            {"name": "app1", "tag": "app1"},
            {"name": "app2", "tag": "app2"}
        ]

        self.services = {}

        for container in containers:
            task_def = ecs.FargateTaskDefinition(self, f"TaskDef-{container['name']}",
                family=f"task-{container['name']}"
            )

            task_def.add_container(f"Container-{container['name']}",
                image=ecs.ContainerImage.from_ecr_repository(ecr_repository1, tag=container["tag"]),
                memory_limit_mib=512,
                cpu=256,
                port_mappings=[ecs.PortMapping(container_port=80)],
                logging=ecs.LogDrivers.aws_logs(
                    stream_prefix="ecs",
                    log_group=log_group
                )
            )

            service = ecs.FargateService(self, f"Service-{container['name']}",
                cluster=self.cluster,
                task_definition=task_def,
                desired_count=1,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                service_name=f"servicio-{container['name']}"
            )

            scaling = service.auto_scale_task_count(min_capacity=1, max_capacity=3)
            scaling.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=80)

            self.services[container["name"]] = service


        self.service1 = self.services["app1"]

