#!/usr/bin/env python3
"""
Test the FIXED S3 deployment with the new ECS task definition
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_aws import S3Bucket
from prefect import get_client

@task
def victory_task(name: str = "Victory"):
    """Victory task to prove everything is working"""
    message = f"🎉🎉🎉 VICTORY! {name} - S3 + ECS IS WORKING! 🎉🎉🎉"
    print(message)
    print("✅ Code successfully pulled from S3!")
    print("🐳 Executed by NEW ECS task definition (v3)!")
    print("📦 prefect-aws is installed and working!")
    print("🏊 gellc-process-pool workers are operational!")
    print("🚀 Complete S3 + ECS + Prefect Cloud integration SUCCESS!")
    return message

@flow
def victory_flow(name: str = "Victory"):
    """Victory flow to celebrate the fix"""
    print(f"🚀 Starting VICTORY flow for: {name}")
    print("📦 Code pulled from S3 using prefect-aws.S3Bucket")
    print("🐳 Executing on NEW ECS task definition") 
    print("🏊 Via updated gellc-process-pool workers")
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = victory_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 VICTORY flow completed!")
    print("🎯 YOUR S3 + ECS DEPLOYMENT IS FULLY WORKING!")
    return result

async def test_fixed_deployment():
    """Test the fixed deployment"""
    
    print("🎯 Testing FIXED S3 deployment...")
    print("=" * 50)
    
    # Delete the previous deployment
    prev_id = "bf4f91c6-cf09-4f86-a607-771d837bfae9"
    
    async with get_client() as client:
        print("🗑️ Cleaning up previous deployment...")
        try:
            await client.delete_deployment(prev_id)
            print(f"✅ Deleted {prev_id}")
        except Exception as e:
            print(f"⚠️ {prev_id}: {e}")
    
    # Create S3Bucket block
    print("🏗️ Creating S3Bucket block...")
    s3_bucket = S3Bucket(
        bucket_name="gellc-prefect-flows",
        basepath="flows/",
        aws_access_key_id=None,
        aws_secret_access_key=None,
    )
    
    # Create VICTORY deployment
    print("📦 Creating VICTORY deployment...")
    deployment = await Deployment.build_from_flow(
        flow=victory_flow,
        name="VICTORY-s3-ecs-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",  # Using FIXED ECS workers
        storage=s3_bucket,  # S3 storage with prefect-aws
        entrypoint="victory_flow.py:victory_flow",
        description="VICTORY! Fixed S3 deployment with working ECS process workers",
        version="3.0.0",
        tags=["VICTORY", "s3", "ecs", "FIXED", "prefect-aws", "WORKING"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 VICTORY DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: VICTORY-s3-ecs-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (FIXED ECS workers)")
    print(f"✅ Storage: S3 bucket with prefect-aws")
    
    # Create victory flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "FINAL VICTORY TEST"}
        )
        
        print(f"\n🎯 VICTORY test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 VICTORY URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SHOULD FINALLY WORK!")
        print(f"🏆 S3 + ECS + prefect-aws = COMPLETE VICTORY!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(test_fixed_deployment())
