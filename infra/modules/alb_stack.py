import os
import json
from aws_cdk import Stack, Duration, CfnOutput
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from constructs import Construct

class AlbStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, ecs_service1: ecs.FargateService, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        load_balancer_name = os.getenv("LOAD_BALANCER_NAME")
        allowed_ips = os.getenv("ALLOWED_IPS", "[]")

        alb_sg = ec2.SecurityGroup(self, "AlbSG",
            vpc=vpc,
            description="Allow HTTP only from trusted public IPs",
            allow_all_outbound=True
        )

        for i, ip in enumerate(allowed_ips):
            alb_sg.add_ingress_rule(
                peer=ec2.Peer.ipv4(ip),
                connection=ec2.Port.tcp(80),
                description=f"Allow HTTP from {ip}"
            )

        alb = elbv2.ApplicationLoadBalancer(self, "ALB1",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            load_balancer_name=load_balancer_name,
            security_group=alb_sg
        )

        target_group = elbv2.ApplicationTargetGroup(self, "TargetGroup",
            vpc=vpc,
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[ecs_service1],
            health_check=elbv2.HealthCheck(
                path="/health_check",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_http_codes="200"
            )
        )

        alb.add_listener("ListenerHTTP",
            port=80,
            default_action=elbv2.ListenerAction.forward([target_group])
        )

        CfnOutput(self, "ALBDnsOutput",
            value=alb.load_balancer_dns_name,
            export_name="ALBDnsName"
        )
