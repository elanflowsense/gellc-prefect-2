#!/usr/bin/env python3
"""
Create deployment using built-in S3 filesystem (not S3Bucket block)
This should work with process workers without requiring prefect-aws
"""
import asyncio
import boto3
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect import get_client

@task
def process_s3_task(name: str = "Process S3"):
    """Task for process execution with S3 storage"""
    message = f"🎉 Hello {name} from PROCESS POOL with S3 storage!"
    print(message)
    print("✅ This is running via process pool workers!")
    print("📦 Code pulled from S3 using built-in S3 filesystem!")
    print("🚀 S3 + Process + Prefect Cloud integration!")
    return message

@flow
def process_s3_flow(name: str = "Process S3"):
    """Flow for process execution with S3 storage"""
    print(f"🚀 Starting PROCESS + S3 flow for: {name}")
    print("📦 Code pulled from S3 bucket using built-in filesystem")
    print("🏗️ Executing via PROCESS workers") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = process_s3_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 PROCESS + S3 flow completed successfully!")
    return result

async def create_process_s3_deployment():
    """Create deployment with process pool and built-in S3 filesystem"""
    
    print("🚀 Creating deployment with process pool + built-in S3...")
    print("=" * 60)
    
    # Delete previous deployment first
    previous_deployment_id = "f0e01792-f2cb-4cbf-9284-5604f614e1a5"
    
    async with get_client() as client:
        print("🗑️ Deleting previous deployment...")
        try:
            await client.delete_deployment(previous_deployment_id)
            print("✅ Previous deployment deleted")
        except Exception as e:
            print(f"⚠️ Previous deployment deletion: {e}")
    
    # Create S3 filesystem (built-in, no prefect-aws needed)
    print("🏗️ Creating built-in S3 filesystem...")
    s3_storage = S3(
        bucket_path="gellc-prefect-flows/flows",
        aws_access_key_id=None,  # Use default AWS credentials
        aws_secret_access_key=None,
    )
    
    # Create deployment with process pool
    print("📦 Creating deployment with gellc-process-pool...")
    deployment = await Deployment.build_from_flow(
        flow=process_s3_flow,
        name="FIXED-process-s3-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",  # Use process pool with active workers
        storage=s3_storage,  # Built-in S3 filesystem
        entrypoint="process_s3_flow.py:process_s3_flow",
        description="S3 deployment using process pool with built-in S3 filesystem",
        version="1.2.0",
        tags=["FIXED", "s3", "process", "built-in-s3"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 FIXED deployment created!")
    print(f"✅ Deployment Name: FIXED-process-s3-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (with active workers)")
    print(f"✅ Storage: Built-in S3 filesystem (no prefect-aws required)")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "Fixed Process Test"}
        )
        
        print(f"\n🎯 Test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 FIXED Deployment URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 This should work without the S3Bucket block error!")
        print(f"🏊 Using: gellc-process-pool with built-in S3 filesystem")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_process_s3_deployment())
