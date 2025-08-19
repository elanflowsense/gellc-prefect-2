#!/usr/bin/env python3
"""
Create a simple deployment without any storage complications
"""
import asyncio
from prefect import flow, task, get_client

@task
def simple_task(name: str = "Simple"):
    """Simple task that should work in containers"""
    import os
    message = f"🎉 SUCCESS! {name} from ECS Container!"
    print(message)
    print(f"✅ Current working directory: {os.getcwd()}")
    print(f"📁 Files in current directory: {os.listdir('.')}")
    print("🐳 Running in ECS container successfully!")
    return message

@flow
def simple_flow(name: str = "Simple"):
    """Simple flow that should work"""
    print(f"🚀 Starting SIMPLE flow for: {name}")
    print("🐳 ECS container execution") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = simple_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 SIMPLE flow completed successfully!")
    return result

async def create_simple_deployment():
    """Create a simple deployment using default settings"""
    
    print("🚀 Creating simple deployment...")
    print("=" * 40)
    
    # Create deployment with minimal configuration
    print("📦 Creating simple deployment...")
    
    from prefect.deployments import Deployment
    
    deployment = Deployment(
        name="SIMPLE-working-deployment",
        flow=simple_flow,
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        tags=["SIMPLE", "working", "minimal"],
        description="Simple deployment that should work in ECS containers",
        version="1.0.0"
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 SIMPLE DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: SIMPLE-working-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool")
    print(f"✅ Configuration: Minimal/Default")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "SIMPLE TEST"}
        )
        
        print(f"\n🎯 Simple test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 SIMPLE DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SHOULD BE THE SIMPLEST WORKING VERSION!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_simple_deployment())
