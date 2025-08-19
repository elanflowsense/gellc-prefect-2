#!/usr/bin/env python3
"""
Create ECS work pool in Prefect Cloud
"""
import asyncio
from prefect import get_client
from prefect.client.schemas.actions import WorkPoolCreate

async def create_ecs_work_pool():
    """Create an ECS work pool in Prefect Cloud"""
    
    work_pool_name = "gellc-ecs-pool"
    
    print(f"🏊 Creating ECS work pool: {work_pool_name}")
    
    try:
        async with get_client() as client:
            # Create ECS work pool using WorkPoolCreate
            work_pool_data = WorkPoolCreate(
                name=work_pool_name,
                type="ecs",
                description="ECS work pool for GELLC Prefect flows",
                base_job_template={
                    "job_configuration": {
                        "command": ["./start.sh"],
                        "family": "gellc-prefect-task",
                        "image": "576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
                        "cluster": "gellc-prefect-cluster",
                        "cpu": 256,
                        "memory": 512,
                        "taskRoleArn": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
                        "executionRoleArn": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
                        "launchType": "FARGATE",
                        "networkConfiguration": {
                            "awsvpcConfiguration": {
                                "subnets": ["subnet-74ebae28", "subnet-30f38b57"],
                                "securityGroups": ["sg-07df2040c0081cac5"],
                                "assignPublicIp": "ENABLED"
                            }
                        },
                        "region": "us-east-1",
                        "env": {
                            "PYTHONPATH": "/app",
                            "PREFECT_MODE": "worker",
                            "PREFECT_WORK_POOL": "gellc-ecs-pool",
                            "PREFECT_API_URL": "https://api.prefect.cloud/api/accounts/ab61b83d-af98-4940-ac58-024d88160a03/workspaces/e31cc9e9-de96-4558-acdc-1ded94493b8d",
                            "PREFECT_API_KEY": "pnu_Mt1EbbVRvkQ8abHqFrhA2BRZJrsg803AcJOR"
                        }
                    },
                    "variables": {
                        "properties": {
                            "image": {
                                "title": "Image",
                                "description": "Docker image to use for the task",
                                "type": "string",
                                "default": "576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest"
                            },
                            "cpu": {
                                "title": "CPU",
                                "description": "CPU units to allocate",
                                "type": "integer",
                                "default": 256
                            },
                            "memory": {
                                "title": "Memory",
                                "description": "Memory in MB to allocate",
                                "type": "integer",
                                "default": 512
                            }
                        },
                        "type": "object"
                    }
                }
            )
            
            work_pool = await client.create_work_pool(work_pool=work_pool_data)
            
            print(f"✅ Successfully created ECS work pool: {work_pool.name}")
            print(f"🔗 Work pool ID: {work_pool.id}")
            print(f"📋 Type: {work_pool.type}")
            
            return work_pool
            
    except Exception as e:
        print(f"❌ Failed to create ECS work pool: {e}")
        return None

if __name__ == "__main__":
    work_pool = asyncio.run(create_ecs_work_pool())
    if work_pool:
        print("\n🎉 Work pool created successfully!")
        print("\nNext steps:")
        print("1. Update ECS task definition with Prefect Cloud credentials")
        print("2. Deploy flows to Prefect Cloud")
        print("3. Start ECS worker to handle flow runs")
    else:
        print("❌ Failed to create work pool")
