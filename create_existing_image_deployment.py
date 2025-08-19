#!/usr/bin/env python3
"""
Create a deployment that uses an existing pre-built Docker image
"""
import asyncio
from prefect import flow, task, get_client
from prefect.docker import DockerImage

@task
def existing_task(name: str = "Existing"):
    """Task running in existing Docker image"""
    import os
    message = f"🎉 SUCCESS! {name} from Existing Docker Image!"
    print(message)
    print(f"✅ Current working directory: {os.getcwd()}")
    print(f"📁 Files in current directory: {os.listdir('.')}")
    print("🐳 Running from existing Docker image in ECS!")
    return message

@flow
def existing_flow(name: str = "Existing"):
    """Flow running in existing Docker image"""
    print(f"🚀 Starting EXISTING IMAGE flow for: {name}")
    print("🐳 ECS execution from existing Docker image") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = existing_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 EXISTING IMAGE flow completed successfully!")
    return result

async def create_existing_image_deployment():
    """Create deployment using existing Docker image"""
    
    print("🚀 Creating deployment with existing Docker image...")
    print("=" * 60)
    
    # Use DockerImage to specify existing image without building
    print("📦 Using existing Docker image...")
    docker_image = DockerImage(
        name="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
        platform="linux/amd64"
    )
    
    deployment_id = await existing_flow.deploy(
        name="EXISTING-image-deployment",
        work_pool_name="gellc-ecs-final",  # Use the ECS work pool
        work_queue_name="default",
        image=docker_image,
        tags=["EXISTING", "docker", "ecs", "working"],
        description="Deployment using existing Docker image",
        version="5.0.0"
    )
    
    print(f"\n🎉 EXISTING IMAGE DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: EXISTING-image-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-ecs-final (ECS)")
    print(f"✅ Image: 576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "EXISTING IMAGE TEST"}
        )
        
        print(f"\n🎯 Existing image test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 EXISTING IMAGE DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS USES EXISTING DOCKER IMAGE WITHOUT BUILDING!")
        print(f"🐳 Should work with ECS work pool and existing image!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_existing_image_deployment())
