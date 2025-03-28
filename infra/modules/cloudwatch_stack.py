from aws_cdk import Stack
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_ecs as ecs
from constructs import Construct

class CloudWatchStack(Stack):
    def __init__(self, scope: Construct, id: str, ecs_services: dict[str, ecs.FargateService], **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dashboard = cloudwatch.Dashboard(self, "EcsDashboard")

        for name, service in ecs_services.items():
            
            cpu_metric = service.metric_cpu_utilization(statistic="Average")

            memory_metric = service.metric_memory_utilization(statistic="Average")

            cpu_alarm = cloudwatch.Alarm(self, f"{name}-CpuAlarm",
                metric=cpu_metric,
                threshold=70,
                evaluation_periods=2,
                datapoints_to_alarm=2,
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                alarm_description=f"High CPU for ECS service {name}"
            )

            dashboard.add_widgets(
                cloudwatch.GraphWidget(
                    title=f"{name} - CPU Utilization",
                    left=[cpu_metric]
                ),
                cloudwatch.GraphWidget(
                    title=f"{name} - Memory Utilization",
                    left=[memory_metric]
                ),
                cloudwatch.AlarmWidget(
                    title=f"{name} - CPU Alarm",
                    alarm=cpu_alarm
                )
            )
