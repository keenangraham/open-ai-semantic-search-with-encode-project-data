from aws_cdk import App
from aws_cdk import Duration
from aws_cdk import Environment
from aws_cdk import Stack

from constructs import Construct


from aws_cdk.aws_certificatemanager import Certificate

from aws_cdk.aws_ec2 import Vpc

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions

from aws_cdk.aws_ecs import AwsLogDriverMode
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import DeploymentCircuitBreaker
from aws_cdk.aws_ecs import LogDriver
from aws_cdk.aws_ecs import PortMapping
from aws_cdk.aws_ecs import Secret

from aws_cdk.aws_secretsmanager import Secret as SMSecret

from aws_cdk.aws_route53 import HostedZone

from typing import Any


US_WEST_2 = Environment(
    account='109189702753',
    region='us-west-2',
)


class SemanticSearch(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        frontend_image = ContainerImage.from_asset(
            '../',
            file='./docker/frontend/Dockerfile',
        )
        backend_image = ContainerImage.from_asset(
            '../',
            file='./docker/backend/Dockerfile',
        )
        vpc = Vpc.from_lookup(
            self,
            'DemoVpc',
            vpc_id='vpc-0b5e3b97317057133'
        )
        certificate = Certificate.from_certificate_arn(
            self,
            'DomainCertificate',
            'arn:aws:acm:us-west-2:109189702753:certificate/6bee1171-2028-43eb-aab8-d992da3c60df'
        )
        zone = HostedZone.from_lookup(
            self,
            'DomainZone',
            domain_name='demo.igvf.org',
        )
        fargate = ApplicationLoadBalancedFargateService(
            self,
            'Fargate',
            service_name='semantic-search',
            vpc=vpc,
            cpu=1024,
            memory_limit_mib=3072,
            desired_count=1,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                container_name='frontend',
                container_port=3000,
                image=frontend_image,
                environment={
                    'BACKEND_URL': 'http://localhost:8000',
                },
                log_driver=LogDriver.aws_logs(
                    stream_prefix='frontend',
                    mode=AwsLogDriverMode.NON_BLOCKING,
                ),
            ),
            public_load_balancer=True,
            assign_public_ip=True,
            certificate=certificate,
            domain_zone=zone,
            domain_name='semantic-search.demo.igvf.org',
            redirect_http=True,
        )
        openai_api_key_secret = SMSecret.from_secret_complete_arn(
            self,
            'OpenAIAPIKeySecret',
            'arn:aws:secretsmanager:us-west-2:109189702753:secret:keenan-openai-api-key-flXPVD',
        )
        fargate.task_definition.add_container(
            'backend',
            container_name='backend',
            image=backend_image,
            port_mappings=[
                PortMapping(
                    container_port=8000
                )
            ],
            environment={
                'DATA_SOURCE': '/data/datasets',
            },
            secrets={
                'OPENAI_API_KEY': Secret.from_secrets_manager(
                    openai_api_key_secret,
                    'OPENAI_API_KEY',
                )
            },
            logging=LogDriver.aws_logs(
                stream_prefix='backend',
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )
        fargate.target_group.configure_health_check(
            interval=Duration.seconds(60),
        )


app = App()


semantic_search = SemanticSearch(
    app,
    'SemanticSearch',
    env=US_WEST_2,
)


app.synth()
