#!/usr/bin/env python3
"""
Create S3 deployment using modern prefect-aws S3Bucket block
"""
import asyncio
import boto3
from prefect import flow, task
from prefect.deployments import Deployment

@task
def s3_ecs_task(name: str = "S3-ECS"):
    """Task that will run from S3 on ECS"""
    message = f"🎉 Hello {name} from S3 + ECS!"
    print(message)
    print("✅ This flow is running on ECS infrastructure!")
    print("📦 Code pulled from S3 and executed on AWS ECS!")
    print("🚀 S3 + ECS + Prefect Cloud = Powerful AWS Integration!")
    return message

@flow
def s3_ecs_flow(name: str = "S3 ECS World"):
    """Flow that will be stored in S3 and run on ECS"""
    print(f"🚀 Starting S3 flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing on ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    print("🔄 All AWS services working together!")
    
    result = s3_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 S3-ECS flow completed successfully!")
    return result

def create_s3_bucket_and_upload():
    """Create S3 bucket and upload flow files"""
    
    bucket_name = "gellc-prefect-flows"
    region = "us-east-1"  # Same as your ECS
    
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"✅ S3 bucket '{bucket_name}' already exists")
        except:
            # Create bucket
            print(f"📦 Creating S3 bucket: {bucket_name}")
            if region == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"✅ S3 bucket created: {bucket_name}")
        
        # Create flow file content
        flow_content = '''from prefect import flow, task

@task
def s3_hello_task(name: str = "S3-ECS"):
    """Simple task for testing S3+ECS execution"""
    message = f"🎉 Hello {name} from S3 + ECS!"
    print(message)
    print("✅ This flow is running on ECS infrastructure!")
    print("📦 Code pulled from S3 and executed on AWS ECS!")
    print("🚀 S3 + ECS + Prefect Cloud = Success!")
    return message

@flow
def s3_hello_flow(name: str = "S3 ECS"):
    """Flow stored in S3 and executed on ECS"""
    print(f"🚀 Starting S3 flow for: {name}")
    print("📦 Code pulled from S3 bucket")
    print("🏗️ Executing on ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = s3_hello_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 Flow completed successfully!")
    return result
'''
        
        # Upload flow file to S3
        print("📤 Uploading flow file to S3...")
        s3_client.put_object(
            Bucket=bucket_name,
            Key="flows/s3_hello_flow.py",
            Body=flow_content,
            ContentType="text/plain"
        )
        
        # Upload requirements.txt with prefect-aws
        requirements_content = """prefect>=2.0.0
boto3>=1.26.0
s3fs>=2023.1.0
prefect-aws>=0.4.0"""
        s3_client.put_object(
            Bucket=bucket_name,
            Key="requirements.txt",
            Body=requirements_content,
            ContentType="text/plain"
        )
        
        print(f"✅ Flow files uploaded to S3: s3://{bucket_name}/flows/")
        return bucket_name
        
    except Exception as e:
        print(f"❌ Error setting up S3: {e}")
        print("\n💡 Make sure you have AWS credentials configured:")
        print("   - AWS CLI configured (aws configure)")
        print("   - Or IAM role attached to your system")
        print("   - Or environment variables set")
        return None

async def create_s3_bucket_block():
    """Create S3Bucket block using modern prefect-aws"""
    
    print("🏗️ Creating S3Bucket block...")
    
    try:
        from prefect_aws import S3Bucket
        from prefect import get_client
        
        # Create S3Bucket block
        s3_bucket = S3Bucket(
            bucket_name="gellc-prefect-flows",
            basepath="flows/",
            aws_access_key_id=None,  # Use default credentials
            aws_secret_access_key=None,  # Use default credentials
        )
        
        # Save the block
        async with get_client() as client:
            block_doc_id = await s3_bucket.save(
                name="gellc-s3-storage",
                overwrite=True
            )
            
        print(f"✅ S3Bucket block created: {block_doc_id}")
        return s3_bucket
        
    except ImportError:
        print("❌ prefect-aws not installed. Installing...")
        import subprocess
        subprocess.run(["pip", "install", "prefect-aws>=0.4.0"])
        
        # Try again after installation
        from prefect_aws import S3Bucket
        from prefect import get_client
        
        s3_bucket = S3Bucket(
            bucket_name="gellc-prefect-flows",
            basepath="flows/",
            aws_access_key_id=None,
            aws_secret_access_key=None,
        )
        
        async with get_client() as client:
            block_doc_id = await s3_bucket.save(
                name="gellc-s3-storage",
                overwrite=True
            )
            
        print(f"✅ S3Bucket block created: {block_doc_id}")
        return s3_bucket
        
    except Exception as e:
        print(f"❌ Error creating S3Bucket block: {e}")
        import traceback
        traceback.print_exc()
        return None

async def create_modern_s3_deployment():
    """Create deployment using modern S3Bucket block"""
    
    print("📦 Creating modern S3-based deployment for ECS...")
    
    # Set up S3 bucket and files
    bucket_name = create_s3_bucket_and_upload()
    if not bucket_name:
        return None
    
    # Create S3Bucket block
    s3_bucket = await create_s3_bucket_block()
    if not s3_bucket:
        return None
    
    try:
        # Create deployment using S3Bucket block
        deployment = await Deployment.build_from_flow(
            flow=s3_ecs_flow,
            name="s3-ecs-flow-modern",
            work_queue_name="default",  
            work_pool_name="gellc-ecs-pool",
            storage=s3_bucket,
            entrypoint="s3_hello_flow.py:s3_hello_flow",
            description="Flow running from S3 on ECS using modern prefect-aws",
            version="2.0.0",
            tags=["s3", "ecs", "aws", "production", "docker", "modern"]
        )
        
        deployment_id = await deployment.apply()
        print(f"✅ Modern S3-ECS deployment created: {deployment_id}")
        
        return deployment_id
        
    except Exception as e:
        print(f"❌ Error creating modern S3-ECS deployment: {e}")
        import traceback
        traceback.print_exc()
        return None

async def setup_modern_s3_ecs():
    """Setup modern S3 + ECS deployment"""
    
    print("📦 Modern S3 + ECS Deployment Setup")
    print("=" * 50)
    
    print("\n🔧 What's different in this approach:")
    print("✅ Uses prefect-aws S3Bucket block (not deprecated)")
    print("✅ Compatible with latest Prefect versions")
    print("✅ Requires prefect-aws>=0.4.0 in Docker image")
    print("✅ Better error handling and diagnostics")
    
    print("\n📋 Prerequisites:")
    print("1. Docker image must include prefect-aws>=0.4.0")
    print("2. ECS tasks need AWS credentials/IAM roles for S3 access")
    print("3. S3 bucket accessible from ECS tasks")
    
    deployment_id = await create_modern_s3_deployment()
    
    if deployment_id:
        print(f"\n🎉 Modern S3 + ECS deployment ready!")
        print(f"✅ Deployment ID: {deployment_id}")
        print(f"✅ Name: s3-ecs-flow-modern")
        print(f"✅ Uses: S3Bucket block from prefect-aws")
        
        print(f"\n⚠️  Important: Your Docker image needs to be rebuilt with:")
        print(f"   pip install prefect-aws>=0.4.0")
        
    else:
        print(f"\n❌ Modern S3 setup failed")
    
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(setup_modern_s3_ecs())
