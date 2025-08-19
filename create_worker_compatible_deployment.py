#!/usr/bin/env python3
"""
Create a deployment that's compatible with Process Workers (no storage blocks)
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect import get_client

@task
def worker_compatible_task(name: str = "Worker Compatible"):
    """Task that works with process workers"""
    message = f"🎉 SUCCESS! {name} from Process Workers WITHOUT storage blocks!"
    print(message)
    print("✅ This runs via Process Workers without S3 storage!")
    print("📁 Code executed directly from local/container filesystem!")
    print("🚀 Process Workers + Prefect Cloud integration!")
    return message

@flow
def worker_compatible_flow(name: str = "Worker Compatible"):
    """Flow that works with process workers"""
    print(f"🚀 Starting WORKER COMPATIBLE flow for: {name}")
    print("📁 No S3 storage blocks - direct execution")
    print("🏗️ Executing via Process Workers") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = worker_compatible_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 WORKER COMPATIBLE flow completed!")
    return result

async def create_worker_compatible_deployment():
    """Create deployment compatible with Process Workers"""
    
    print("🚀 Creating Process Worker compatible deployment...")
    print("=" * 60)
    
    # Delete the problematic S3 deployment
    s3_deployment_id = "8fb1cac6-0493-4da7-aacf-6383690fa2b1"
    
    async with get_client() as client:
        print("🗑️ Deleting S3 deployment that workers can't handle...")
        try:
            await client.delete_deployment(s3_deployment_id)
            print("✅ S3 deployment deleted")
        except Exception as e:
            print(f"⚠️ S3 deployment deletion: {e}")
    
    # Create worker-compatible deployment (NO STORAGE BLOCKS)
    print("📦 Creating worker-compatible deployment (no storage)...")
    deployment = await Deployment.build_from_flow(
        flow=worker_compatible_flow,
        name="WORKER-compatible-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",
        # NO STORAGE PARAMETER = local execution, compatible with workers
        entrypoint="worker_compatible_flow.py:worker_compatible_flow",
        description="Deployment compatible with Process Workers (no storage blocks)",
        version="2.0.0",
        tags=["WORKER", "compatible", "no-storage", "WORKING"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 WORKER COMPATIBLE DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: WORKER-compatible-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (Process Workers)")
    print(f"✅ Storage: None (local execution)")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "WORKER TEST"}
        )
        
        print(f"\n🎯 Test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 WORKER COMPATIBLE URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SHOULD WORK WITH PROCESS WORKERS!")
        print(f"🏆 No storage blocks = Process Worker compatible!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_worker_compatible_deployment())
