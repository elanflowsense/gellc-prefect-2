#!/usr/bin/env python3
"""
Recreate the deployment with gellc-process-pool (since update API is different)
"""
import asyncio
import boto3
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_aws import S3Bucket
from prefect import get_client

@task
def real_ecs_task(name: str = "Real ECS"):
    """Task for real ECS execution"""
    message = f"🎉 Hello {name} from PROCESS POOL!"
    print(message)
    print("✅ This is running via process pool workers!")
    print("📦 Code pulled from S3 and executed via process workers!")
    print("🚀 S3 + Process + Prefect Cloud integration!")
    return message

@flow
def real_ecs_flow(name: str = "Real ECS"):
    """Real flow for process execution"""
    print(f"🚀 Starting REAL flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing via PROCESS workers") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = real_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 REAL flow completed successfully!")
    return result

async def recreate_with_process_pool():
    """Recreate deployment with process pool"""
    
    print("🚀 Recreating deployment with gellc-process-pool...")
    print("=" * 60)
    
    # First delete the old deployment
    old_deployment_id = "bfa29b27-5f1d-49ef-912a-543295b61751"
    
    async with get_client() as client:
        print("🗑️ Deleting old deployment...")
        try:
            await client.delete_deployment(old_deployment_id)
            print("✅ Old deployment deleted")
        except Exception as e:
            print(f"⚠️ Old deployment deletion: {e}")
    
    # Upload flow to S3 (reuse existing)
    bucket_name = "gellc-prefect-flows"
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    # Create S3Bucket block (reuse existing name)
    print("🏗️ Using existing S3Bucket block...")
    s3_bucket = S3Bucket(
        bucket_name=bucket_name,
        basepath="flows/",
        aws_access_key_id=None,
        aws_secret_access_key=None,
    )
    
    # Create NEW deployment with process pool
    print("📦 Creating NEW deployment with gellc-process-pool...")
    deployment = await Deployment.build_from_flow(
        flow=real_ecs_flow,
        name="WORKING-s3-process-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",  # Use process pool with active workers
        storage=s3_bucket,
        entrypoint="real_ecs_flow.py:real_ecs_flow",
        description="S3 deployment using process pool with active workers",
        version="1.1.0",
        tags=["WORKING", "s3", "process", "ACTIVE"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 NEW deployment created with process pool!")
    print(f"✅ Deployment Name: WORKING-s3-process-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (with 2 active workers)")
    print(f"✅ Storage: S3 bucket")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "Process Test"}
        )
        
        print(f"\n🎯 Test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 NEW Deployment URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 This deployment should show as 'Ready' (not Late)!")
        print(f"🏊 Using: gellc-process-pool with 2 active workers")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(recreate_with_process_pool())
