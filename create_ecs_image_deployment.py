#!/usr/bin/env python3
"""
Create a deployment that uses the ECS work pool with Docker image
"""
import asyncio
from prefect import flow, task, get_client

@task
def ecs_task(name: str = "ECS"):
    """Task running in ECS with Docker image"""
    import os
    message = f"🎉 SUCCESS! {name} from ECS Docker Image!"
    print(message)
    print(f"✅ Current working directory: {os.getcwd()}")
    print(f"📁 Files in current directory: {os.listdir('.')}")
    print("🐳 Running from Docker image in ECS via ECS work pool!")
    return message

@flow
def ecs_flow(name: str = "ECS"):
    """Flow running in ECS with Docker image"""
    print(f"🚀 Starting ECS flow for: {name}")
    print("🐳 ECS execution from Docker image via ECS work pool") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 ECS flow completed successfully!")
    return result

async def create_ecs_image_deployment():
    """Create deployment using ECS work pool with Docker image"""
    
    print("🚀 Creating ECS work pool deployment...")
    print("=" * 50)
    
    # Use flow.deploy() with ECS work pool that supports Docker images
    print("📦 Creating deployment with ECS work pool...")
    
    deployment_id = await ecs_flow.deploy(
        name="ECS-docker-deployment",
        work_pool_name="gellc-ecs-final",  # Use the existing ECS work pool
        work_queue_name="default",
        image="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
        tags=["ECS", "docker", "working", "final"],
        description="Deployment using ECS work pool with Docker image",
        version="4.0.0"
    )
    
    print(f"\n🎉 ECS DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: ECS-docker-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-ecs-final (ECS work pool)")
    print(f"✅ Image: 576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "ECS FINAL TEST"}
        )
        
        print(f"\n🎯 ECS test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 ECS DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS USES ECS WORK POOL WITH DOCKER IMAGE!")
        print(f"💡 This should work since gellc-ecs-final supports Docker images!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_ecs_image_deployment())
