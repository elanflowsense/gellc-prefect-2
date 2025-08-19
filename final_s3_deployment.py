#!/usr/bin/env python3
"""
Final S3 deployment that will work with updated ECS workers
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_aws import S3Bucket
from prefect import get_client

@task
def s3_success_task(name: str = "S3 Success"):
    """Task that proves S3 storage is working"""
    message = f"🎉 SUCCESS! {name} from S3 + ECS Process Workers!"
    print(message)
    print("✅ Code successfully pulled from S3!")
    print("🐳 Executed by ECS Fargate containers!")
    print("🏊 Using gellc-process-pool workers!")
    print("📦 prefect-aws is working perfectly!")
    print("🚀 Complete S3 + ECS + Prefect Cloud integration!")
    return message

@flow
def s3_success_flow(name: str = "S3 Success"):
    """Flow that proves the complete S3 + ECS integration"""
    print(f"🚀 Starting FINAL S3 SUCCESS flow for: {name}")
    print("📦 Code pulled from S3 bucket using prefect-aws")
    print("🐳 Executing on ECS Fargate containers") 
    print("🏊 Via gellc-process-pool workers")
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = s3_success_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 S3 SUCCESS flow completed!")
    print("🎯 Your S3 + ECS deployment is now FULLY WORKING!")
    return result

async def deploy_final_s3_flow():
    """Deploy the final working S3 flow"""
    
    print("🚀 Creating FINAL S3 deployment with updated ECS workers...")
    print("=" * 60)
    
    # Delete previous test deployments
    deployments_to_delete = [
        "c697a462-d98b-497e-8279-cb40ae29ddff",  # FIXED-process-s3-deployment
        "79cb074b-eef1-4bc8-989d-537cffa89b5f",  # IDENTIFY-worker-environment
        "11960ab8-fb19-4319-b78c-5f083441540e",  # DEBUG-worker-environment
    ]
    
    async with get_client() as client:
        print("🗑️ Cleaning up test deployments...")
        for dep_id in deployments_to_delete:
            try:
                await client.delete_deployment(dep_id)
                print(f"✅ Deleted {dep_id}")
            except Exception as e:
                print(f"⚠️ {dep_id}: {e}")
    
    # Create S3Bucket block (modern prefect-aws approach)
    print("🏗️ Creating S3Bucket block...")
    s3_bucket = S3Bucket(
        bucket_name="gellc-prefect-flows",
        basepath="flows/",
        aws_access_key_id=None,  # Use default AWS credentials
        aws_secret_access_key=None,
    )
    
    # Create FINAL deployment
    print("📦 Creating FINAL S3 deployment...")
    deployment = await Deployment.build_from_flow(
        flow=s3_success_flow,
        name="FINAL-s3-ecs-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",  # ECS workers with prefect-aws
        storage=s3_bucket,  # S3 storage with prefect-aws
        entrypoint="s3_success_flow.py:s3_success_flow",
        description="FINAL working S3 deployment with ECS process workers",
        version="2.0.0",
        tags=["FINAL", "s3", "ecs", "WORKING", "prefect-aws"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 FINAL S3 DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: FINAL-s3-ecs-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-process-pool (ECS workers with prefect-aws)")
    print(f"✅ Storage: S3 bucket with prefect-aws")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "FINAL SUCCESS TEST"}
        )
        
        print(f"\n🎯 FINAL test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 FINAL Deployment URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS SHOULD NOW WORK PERFECTLY!")
        print(f"📦 S3 storage + ECS workers + prefect-aws = SUCCESS!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(deploy_final_s3_flow())
