#!/usr/bin/env python3
"""
Create a deployment that specifies the Docker image for ECS
"""
import asyncio
from prefect import flow, task, get_client

@task
def image_task(name: str = "Image"):
    """Task running from Docker image"""
    import os
    message = f"🎉 SUCCESS! {name} from Docker Image!"
    print(message)
    print(f"✅ Current working directory: {os.getcwd()}")
    print(f"📁 Files in current directory: {os.listdir('.')}")
    print("🐳 Running from Docker image in ECS container!")
    return message

@flow
def image_flow(name: str = "Image"):
    """Flow running from Docker image"""
    print(f"🚀 Starting IMAGE flow for: {name}")
    print("🐳 ECS container execution from Docker image") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = image_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 IMAGE flow completed successfully!")
    return result

async def create_image_deployment():
    """Create deployment that specifies the Docker image"""
    
    print("🚀 Creating Docker image deployment...")
    print("=" * 40)
    
    # Use flow.deploy() with Docker image specification
    print("📦 Creating deployment with Docker image...")
    
    deployment_id = await image_flow.deploy(
        name="IMAGE-docker-deployment",
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        image="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
        tags=["IMAGE", "docker", "ecs", "working"],
        description="Deployment using Docker image for ECS",
        version="3.0.0"
    )
    
    print(f"\n🎉 IMAGE DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: IMAGE-docker-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool")
    print(f"✅ Image: 576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "IMAGE TEST"}
        )
        
        print(f"\n🎯 Image test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 IMAGE DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SPECIFIES THE DOCKER IMAGE FOR ECS!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_image_deployment())
