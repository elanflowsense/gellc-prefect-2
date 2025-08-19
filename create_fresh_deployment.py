#!/usr/bin/env python3
"""
Create a fresh S3-ECS deployment with a new name
"""
import asyncio
import boto3
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_aws import S3Bucket

@task
def hello_ecs_task(name: str = "ECS World"):
    """Simple task for ECS execution"""
    message = f"🎉 Hello {name} from ECS!"
    print(message)
    print("✅ This flow is running on ECS infrastructure!")
    print("📦 Code pulled from S3 and executed on AWS ECS!")
    print("🚀 S3 + ECS + Prefect Cloud = Success!")
    return message

@flow
def hello_ecs_flow(name: str = "ECS World"):
    """Simple flow for ECS execution"""
    print(f"🚀 Starting flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing on ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = hello_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 Flow completed successfully!")
    return result

async def create_fresh_deployment():
    """Create a brand new deployment"""
    
    print("🚀 Creating fresh S3-ECS deployment...")
    print("=" * 50)
    
    # Upload fresh flow file to S3
    bucket_name = "gellc-prefect-flows"
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    # Create new flow file content
    flow_content = '''from prefect import flow, task

@task
def hello_ecs_task(name: str = "ECS World"):
    """Simple task for ECS execution"""
    message = f"🎉 Hello {name} from ECS!"
    print(message)
    print("✅ This flow is running on ECS infrastructure!")
    print("📦 Code pulled from S3 and executed on AWS ECS!")
    print("🚀 S3 + ECS + Prefect Cloud = Success!")
    return message

@flow
def hello_ecs_flow(name: str = "ECS World"):
    """Simple flow for ECS execution"""
    print(f"🚀 Starting flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing on ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = hello_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 Flow completed successfully!")
    return result
'''
    
    # Upload to S3
    print("📤 Uploading fresh flow to S3...")
    s3_client.put_object(
        Bucket=bucket_name,
        Key="flows/hello_ecs_flow.py",
        Body=flow_content,
        ContentType="text/plain"
    )
    print("✅ Flow uploaded to S3")
    
    # Create S3Bucket block
    print("🏗️ Creating S3Bucket block...")
    s3_bucket = S3Bucket(
        bucket_name=bucket_name,
        basepath="flows/",
        aws_access_key_id=None,  # Use default credentials
        aws_secret_access_key=None,  # Use default credentials
    )
    
    # Save the block with a new name
    block_doc_id = await s3_bucket.save(
        name="fresh-s3-storage",
        overwrite=True
    )
    print(f"✅ S3Bucket block saved: {block_doc_id}")
    
    # Create deployment
    print("📦 Creating deployment...")
    deployment = await Deployment.build_from_flow(
        flow=hello_ecs_flow,
        name="fresh-s3-ecs-deployment",
        work_queue_name="default",  
        work_pool_name="gellc-ecs-pool",
        storage=s3_bucket,
        entrypoint="hello_ecs_flow.py:hello_ecs_flow",
        description="Fresh S3-ECS deployment for testing",
        version="1.0.0",
        tags=["fresh", "s3", "ecs", "working"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 Fresh deployment created successfully!")
    print(f"✅ Deployment Name: fresh-s3-ecs-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Work Pool: gellc-ecs-pool")
    print(f"✅ Storage: S3 bucket")
    
    # Create a test flow run
    from prefect import get_client
    
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "Fresh Test"}
        )
        
        print(f"\n🎯 Test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 Prefect Cloud URLs:")
        print(f"Deployment: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments/deployment/{deployment_id}")
        print(f"Flow Run: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 To find in UI:")
        print(f"1. Go to Deployments page")
        print(f"2. Look for: 'fresh-s3-ecs-deployment'")
        print(f"3. Tags: fresh, s3, ecs, working")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_fresh_deployment())
