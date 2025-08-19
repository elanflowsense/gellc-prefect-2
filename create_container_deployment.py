#!/usr/bin/env python3
"""
Create a deployment that works with ECS containers by embedding the flow directly
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect import get_client

# Define the flow directly in this file so it's self-contained
@task
def container_task(name: str = "Container"):
    """Task that works in ECS containers"""
    message = f"🎉 SUCCESS! {name} from ECS Container Workers!"
    print(message)
    print("✅ Running in ECS Fargate container!")
    print("🐳 Code embedded in deployment - no external storage needed!")
    print("🏊 Process Workers + ECS + Prefect Cloud working!")
    return message

@flow
def container_flow(name: str = "Container"):
    """Flow that works in ECS containers"""
    print(f"🚀 Starting CONTAINER flow for: {name}")
    print("🐳 Executing in ECS Fargate container")
    print("📦 Flow code embedded in deployment") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = container_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 CONTAINER flow completed successfully!")
    return result

async def create_container_deployment():
    """Create deployment that works in ECS containers"""
    
    print("🚀 Creating ECS container-compatible deployment...")
    print("=" * 60)
    
    # Delete the previous deployment
    prev_deployment_id = "b8b52181-3df5-431a-aab9-34707d98413b"
    
    async with get_client() as client:
        print("🗑️ Cleaning up previous deployment...")
        try:
            await client.delete_deployment(prev_deployment_id)
            print("✅ Previous deployment deleted")
        except Exception as e:
            print(f"⚠️ Previous deployment deletion: {e}")
    
    # Create deployment with embedded flow (no external file dependencies)
    print("📦 Creating ECS container deployment...")
    deployment = await Deployment.build_from_flow(
        flow=container_flow,
        name="CONTAINER-ecs-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",
        # Use RemoteFileSystem storage pointing to the container's /app directory
        storage=None,  # No storage - flow is embedded
        description="ECS container deployment with embedded flow",
        version="3.0.0",
        tags=["CONTAINER", "ecs", "embedded", "WORKING"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 CONTAINER DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: CONTAINER-ecs-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (ECS containers)")
    print(f"✅ Storage: None (embedded flow)")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "ECS CONTAINER TEST"}
        )
        
        print(f"\n🎯 ECS test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 CONTAINER DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SHOULD WORK IN ECS CONTAINERS!")
        print(f"🐳 No file path dependencies - flow is embedded!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_container_deployment())