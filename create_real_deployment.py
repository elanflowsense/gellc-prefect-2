#!/usr/bin/env python3
"""
Create a deployment in your REAL Prefect Cloud account using existing work pools
"""
import asyncio
import boto3
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_aws import S3Bucket

@task
def real_ecs_task(name: str = "Real ECS"):
    """Task for real ECS execution"""
    message = f"🎉 Hello {name} from REAL ECS!"
    print(message)
    print("✅ This is running on your REAL ECS infrastructure!")
    print("📦 Code pulled from S3 and executed on AWS ECS!")
    print("🚀 Real S3 + ECS + Prefect Cloud integration!")
    return message

@flow
def real_ecs_flow(name: str = "Real ECS"):
    """Real flow for your ECS execution"""
    print(f"🚀 Starting REAL flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing on REAL ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = real_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 REAL flow completed successfully!")
    return result

async def create_real_deployment():
    """Create deployment in your real account"""
    
    print("🚀 Creating REAL S3-ECS deployment in your account...")
    print("=" * 60)
    
    # Upload flow to S3
    bucket_name = "gellc-prefect-flows"
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    flow_content = '''from prefect import flow, task

@task
def real_ecs_task(name: str = "Real ECS"):
    """Task for real ECS execution"""
    message = f"🎉 Hello {name} from REAL ECS!"
    print(message)
    print("✅ This is running on your REAL ECS infrastructure!")
    print("📦 Code pulled from S3 and executed on AWS ECS!")
    print("🚀 Real S3 + ECS + Prefect Cloud integration!")
    return message

@flow
def real_ecs_flow(name: str = "Real ECS"):
    """Real flow for your ECS execution"""
    print(f"🚀 Starting REAL flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing on REAL ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = real_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 REAL flow completed successfully!")
    return result
'''
    
    print("📤 Uploading flow to S3...")
    s3_client.put_object(
        Bucket=bucket_name,
        Key="flows/real_ecs_flow.py",
        Body=flow_content,
        ContentType="text/plain"
    )
    print("✅ Flow uploaded to S3")
    
    # Create S3Bucket block
    print("🏗️ Creating S3Bucket block...")
    s3_bucket = S3Bucket(
        bucket_name=bucket_name,
        basepath="flows/",
        aws_access_key_id=None,
        aws_secret_access_key=None,
    )
    
    block_doc_id = await s3_bucket.save(
        name="real-s3-storage",
        overwrite=True
    )
    print(f"✅ S3Bucket block saved: {block_doc_id}")
    
    # Create deployment using existing work pool
    print("📦 Creating deployment with gellc-ecs-final work pool...")
    deployment = await Deployment.build_from_flow(
        flow=real_ecs_flow,
        name="REAL-s3-ecs-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-ecs-final",  # Use your existing ECS work pool
        storage=s3_bucket,
        entrypoint="real_ecs_flow.py:real_ecs_flow",
        description="REAL S3-ECS deployment in your actual Prefect Cloud account",
        version="1.0.0",
        tags=["REAL", "s3", "ecs", "working", "VISIBLE"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 REAL deployment created in your account!")
    print(f"✅ Deployment Name: REAL-s3-ecs-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-ecs-final")
    print(f"✅ Storage: S3 bucket")
    
    # Create test flow run
    from prefect import get_client
    
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "REAL Test"}
        )
        
        print(f"\n🎯 Test flow run created in your account:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 YOUR ACTUAL Prefect Cloud URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 To find in YOUR UI:")
        print(f"1. Go to: {base_url}/deployments")
        print(f"2. Look for: 'REAL-s3-ecs-deployment'")
        print(f"3. Tags: REAL, s3, ecs, working, VISIBLE")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_real_deployment())
