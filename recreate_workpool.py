#!/usr/bin/env python3
"""
Recreate the ECS work pool with correct configuration
"""
import asyncio
from prefect import get_client
from prefect.client.schemas.actions import WorkPoolCreate

async def recreate_ecs_work_pool():
    """Delete and recreate the ECS work pool with correct configuration"""
    
    print("🗑️  Deleting existing work pool...")
    
    try:
        async with get_client() as client:
            # Delete the existing work pool
            await client.delete_work_pool("gellc-ecs-pool")
            print("✅ Deleted existing work pool")
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Create new work pool with correct configuration
            print("🏊 Creating new ECS work pool with correct configuration...")
            
            work_pool_data = WorkPoolCreate(
                name="gellc-ecs-pool",
                type="ecs",
                description="ECS work pool for GELLC Prefect flows - Fixed",
                base_job_template={
                    "job_configuration": {
                        "command": "./start.sh",  # STRING, not list!
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
                            "PREFECT_MODE": "flow",  # Changed to flow mode for ECS tasks
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
            
            print(f"✅ Successfully recreated ECS work pool: {work_pool.name}")
            print(f"🔗 Work pool ID: {work_pool.id}")
            print(f"🔧 Command is now a string: './start.sh'")
            
            return work_pool
            
    except Exception as e:
        print(f"❌ Error recreating work pool: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    work_pool = asyncio.run(recreate_ecs_work_pool())
    if work_pool:
        print("\n🎉 Work pool recreated successfully!")
        print("🚀 Now try running your flow again - it should work!")
    else:
        print("❌ Failed to recreate work pool")
