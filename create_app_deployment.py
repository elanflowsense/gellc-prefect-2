#!/usr/bin/env python3
"""
Create a deployment that uses the container's /app directory
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import LocalFileSystem
from prefect import get_client

@task
def app_task(name: str = "App"):
    """Task that works from /app directory"""
    message = f"🎉 SUCCESS! {name} from /app directory in ECS!"
    print(message)
    print("✅ Running from /app directory in ECS container!")
    print("📁 Using container's working directory!")
    print("🐳 ECS + Process Workers + /app = SUCCESS!")
    return message

@flow
def app_flow(name: str = "App"):
    """Flow that works from /app directory"""
    print(f"🚀 Starting /APP flow for: {name}")
    print("📁 Working from /app directory in container")
    print("🐳 ECS container execution") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = app_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 /APP flow completed successfully!")
    return result

async def create_app_deployment():
    """Create deployment that uses /app directory"""
    
    print("🚀 Creating /app directory deployment...")
    print("=" * 50)
    
    # Delete the previous deployment
    prev_deployment_id = "a07fd9a6-fa42-4c82-b8c3-12e960822e3c"
    
    async with get_client() as client:
        print("🗑️ Cleaning up previous deployment...")
        try:
            await client.delete_deployment(prev_deployment_id)
            print("✅ Previous deployment deleted")
        except Exception as e:
            print(f"⚠️ Previous deployment deletion: {e}")
    
    # Create LocalFileSystem storage pointing to /app (container's working directory)
    print("📁 Creating LocalFileSystem storage for /app...")
    local_storage = LocalFileSystem(basepath="/app")
    
    # Create deployment using /app directory
    print("📦 Creating /app deployment...")
    deployment = await Deployment.build_from_flow(
        flow=app_flow,
        name="APP-directory-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",
        storage=local_storage,  # Use /app directory in container
        entrypoint="app_flow.py:app_flow",  # This will be relative to /app
        description="Deployment using /app directory in ECS container",
        version="4.0.0",
        tags=["APP", "ecs", "directory", "WORKING"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 /APP DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: APP-directory-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (ECS containers)")
    print(f"✅ Storage: LocalFileSystem(/app)")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "APP DIRECTORY TEST"}
        )
        
        print(f"\n🎯 /app test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 /APP DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SHOULD WORK FROM /APP DIRECTORY!")
        print(f"📁 Uses container's /app working directory!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_app_deployment())
