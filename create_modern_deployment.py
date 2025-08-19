#!/usr/bin/env python3
"""
Create a deployment using the modern flow.deploy() method
"""
import asyncio
from prefect import flow, task, get_client

@task
def modern_task(name: str = "Modern"):
    """Modern task using flow.deploy()"""
    import os
    message = f"🎉 SUCCESS! {name} from Modern Deployment!"
    print(message)
    print(f"✅ Current working directory: {os.getcwd()}")
    print(f"📁 Files in current directory: {os.listdir('.')}")
    print("🐳 Running in ECS container via modern deployment!")
    return message

@flow
def modern_flow(name: str = "Modern"):
    """Modern flow using flow.deploy()"""
    print(f"🚀 Starting MODERN flow for: {name}")
    print("🐳 ECS container execution via flow.deploy()") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = modern_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 MODERN flow completed successfully!")
    return result

async def create_modern_deployment():
    """Create deployment using modern flow.deploy() method"""
    
    print("🚀 Creating modern deployment with flow.deploy()...")
    print("=" * 50)
    
    # Use the modern flow.deploy() method
    print("📦 Using flow.deploy() method...")
    
    deployment_id = await modern_flow.deploy(
        name="MODERN-flow-deploy",
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        tags=["MODERN", "flow-deploy", "working"],
        description="Modern deployment using flow.deploy() method",
        version="2.0.0"
    )
    
    print(f"\n🎉 MODERN DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: MODERN-flow-deploy")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool")
    print(f"✅ Method: flow.deploy() (modern)")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "MODERN TEST"}
        )
        
        print(f"\n🎯 Modern test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 MODERN DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS USES THE RECOMMENDED MODERN APPROACH!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_modern_deployment())
