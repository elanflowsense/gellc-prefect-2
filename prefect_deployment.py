"""
Prefect deployment configuration for ECS infrastructure
"""

from prefect import flow
from prefect.deployments import Deployment
from prefect.infrastructure import ECSTask
from prefect.blocks.system import Secret
import os

# Your main flow (from my_prefect_flow.py)
@flow
def my_first_flow():
    from my_prefect_flow import say_hello
    say_hello("World from ECS!")

# ECS Infrastructure configuration
ecs_task = ECSTask(
    # Your AWS account and region
    aws_credentials=None,  # Uses default credentials
    cluster="gellc-prefect-cluster",
    
    # Task definition settings
    family="gellc-prefect-task",
    image="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
    cpu=256,
    memory=512,
    
    # Network configuration
    vpc_id="vpc-b355c1c9",
    subnets=["subnet-74ebae28", "subnet-30f38b57"],
    security_groups=["sg-07df2040c0081cac5"],
    assign_public_ip=True,
    
    # Task settings
    task_role_arn="arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
    execution_role_arn="arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
    
    # Environment variables
    env={"PYTHONPATH": "/app"},
    
    # Launch type
    launch_type="FARGATE",
    
    # Region
    region="us-east-1",
)

# Create deployment
deployment = Deployment.build_from_flow(
    flow=my_first_flow,
    name="gellc-ecs-deployment",
    infrastructure=ecs_task,
    work_queue_name="ecs-queue",
)

if __name__ == "__main__":
    # Save the deployment
    deployment_id = deployment.apply()
    print(f"Deployment created with ID: {deployment_id}")
    
    print("\nECS Infrastructure Summary:")
    print(f"Cluster: gellc-prefect-cluster")
    print(f"Task Definition: gellc-prefect-task")
    print(f"Service: gellc-prefect-service")
    print(f"Public IP: 44.202.220.25")
    print(f"Security Group: sg-07df2040c0081cac5")
    
    print("\nTo run flows:")
    print("1. Start Prefect server: prefect server start")
    print("2. Start an agent: prefect agent start -q ecs-queue")
    print("3. Run a flow: prefect deployment run 'my-first-flow/gellc-ecs-deployment'")
