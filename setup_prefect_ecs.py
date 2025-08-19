"""
Setup script for Prefect ECS integration
"""

from prefect.infrastructure import ECSTask
from prefect.work_pools import WorkPool
from prefect.filesystems import S3
import asyncio

async def setup_ecs_infrastructure():
    """Setup ECS infrastructure block in Prefect"""
    
    # Create ECS Task infrastructure block
    ecs_block = ECSTask(
        block_name="gellc-ecs-task",
        cluster="gellc-prefect-cluster",
        family="gellc-prefect-task", 
        image="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
        cpu=256,
        memory=512,
        vpc_id="vpc-b355c1c9",
        subnets=["subnet-74ebae28", "subnet-30f38b57"],
        security_groups=["sg-07df2040c0081cac5"],
        assign_public_ip=True,
        task_role_arn="arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
        execution_role_arn="arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
        launch_type="FARGATE",
        region="us-east-1",
        env={"PYTHONPATH": "/app"}
    )
    
    # Save the block
    await ecs_block.save("gellc-ecs-task", overwrite=True)
    print("✅ ECS Task infrastructure block saved")
    
    return ecs_block

def create_work_pool():
    """Create ECS work pool configuration"""
    
    work_pool_config = {
        "name": "gellc-ecs-pool",
        "type": "ecs",
        "base_job_template": {
            "job_configuration": {
                "cluster": "gellc-prefect-cluster",
                "family": "gellc-prefect-task",
                "image": "576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
                "cpu": 256,
                "memory": 512,
                "networkConfiguration": {
                    "awsvpcConfiguration": {
                        "subnets": ["subnet-74ebae28", "subnet-30f38b57"],
                        "securityGroups": ["sg-07df2040c0081cac5"],
                        "assignPublicIp": "ENABLED"
                    }
                },
                "taskRoleArn": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
                "executionRoleArn": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
                "launchType": "FARGATE",
                "region": "us-east-1"
            }
        }
    }
    
    return work_pool_config

if __name__ == "__main__":
    # Setup infrastructure
    print("Setting up Prefect ECS infrastructure...")
    
    # Run async setup
    asyncio.run(setup_ecs_infrastructure())
    
    # Print work pool configuration
    work_pool = create_work_pool()
    print("\n✅ Work pool configuration created")
    print("Run this command to create the work pool:")
    print("prefect work-pool create gellc-ecs-pool --type ecs")
    
    print("\n📋 Next steps:")
    print("1. Start Prefect server: prefect server start")
    print("2. Create work pool: prefect work-pool create gellc-ecs-pool --type ecs")
    print("3. Deploy flows: python prefect_deployment.py")
    print("4. Start worker: prefect worker start --pool gellc-ecs-pool")
