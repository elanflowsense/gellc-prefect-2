#!/usr/bin/env python3
"""
Create deployment using local storage with process pool
This avoids any S3 dependencies and should work with existing process workers
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect import get_client

@task
def local_process_task(name: str = "Local Process"):
    """Task for local process execution"""
    message = f"🎉 Hello {name} from LOCAL PROCESS POOL!"
    print(message)
    print("✅ This is running via local process pool workers!")
    print("📁 Using local storage (no S3 dependencies needed)!")
    print("🚀 Local + Process + Prefect Cloud integration!")
    return message

@flow
def local_process_flow(name: str = "Local Process"):
    """Flow for local process execution"""
    print(f"🚀 Starting LOCAL PROCESS flow for: {name}")
    print("📁 Using local file storage")
    print("🏗️ Executing via LOCAL PROCESS workers") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = local_process_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 LOCAL PROCESS flow completed successfully!")
    return result

async def create_local_process_deployment():
    """Create deployment with process pool and local storage"""
    
    print("🚀 Creating deployment with process pool + local storage...")
    print("=" * 60)
    
    # Delete previous deployment first
    previous_deployment_id = "c697a462-d98b-497e-8279-cb40ae29ddff"
    
    async with get_client() as client:
        print("🗑️ Deleting previous deployment...")
        try:
            await client.delete_deployment(previous_deployment_id)
            print("✅ Previous deployment deleted")
        except Exception as e:
            print(f"⚠️ Previous deployment deletion: {e}")
    
    # Create deployment with process pool and local storage (no storage parameter = local)
    print("📦 Creating deployment with gellc-process-pool + local storage...")
    deployment = await Deployment.build_from_flow(
        flow=local_process_flow,
        name="WORKING-local-process-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",  # Use process pool with active workers
        # No storage parameter = uses local storage
        entrypoint="local_process_flow.py:local_process_flow",
        description="Local deployment using process pool with local storage",
        version="1.3.0",
        tags=["WORKING", "local", "process", "no-s3"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 WORKING deployment created!")
    print(f"✅ Deployment Name: WORKING-local-process-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (with active workers)")
    print(f"✅ Storage: Local storage (no dependencies required)")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "Working Local Test"}
        )
        
        print(f"\n🎯 Test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 WORKING Deployment URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 This should work without ANY storage errors!")
        print(f"🏊 Using: gellc-process-pool with local storage")
        print(f"🎯 No S3, no prefect-aws, no block dependencies!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_local_process_deployment())
