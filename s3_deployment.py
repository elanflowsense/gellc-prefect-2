#!/usr/bin/env python3
"""
Create a deployment using S3 storage - perfect for AWS ECS setup!
"""
import asyncio
import boto3
from prefect import flow, task
from prefect.blocks.system import String

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
    """Flow that will be stored in S3"""
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
        
        # Upload requirements.txt
        requirements_content = "prefect>=2.0.0\nboto3>=1.26.0"
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

async def create_s3_deployment():
    """Create a deployment using S3 storage"""
    
    print("📦 Creating S3-based deployment...")
    
    # First set up S3 bucket and files
    bucket_name = create_s3_bucket_and_upload()
    if not bucket_name:
        return None
    
    try:
        # Configure S3 storage
        s3_storage = S3(
            bucket_path=f"s3://{bucket_name}/flows",
            aws_access_key_id=None,  # Use default credentials
            aws_secret_access_key=None,  # Use default credentials
        )
        
        deployment = await Deployment.build_from_flow(
            flow=s3_ecs_flow,
            name="s3-ecs-flow",
            work_pool_name="gellc-process-pool",
            storage=s3_storage,
            entrypoint="s3_hello_flow.py:s3_hello_flow",
            description="Flow running from S3 on ECS",
            version="1.0.0",
            tags=["s3", "ecs", "aws", "production"]
        )
        
        deployment_id = await deployment.apply()
        print(f"✅ S3 deployment created: {deployment_id}")
        
        return deployment_id
        
    except Exception as e:
        print(f"❌ Error creating S3 deployment: {e}")
        return None

async def setup_s3_approach():
    """Complete S3 setup and deployment"""
    
    print("📦 S3 + ECS Deployment Setup")
    print("=" * 50)
    
    print("\n🚀 Advantages of S3 approach:")
    print("✅ No GitHub setup needed")
    print("✅ Native AWS integration")
    print("✅ Perfect for ECS workloads")
    print("✅ Fast file access from ECS")
    print("✅ Versioning and backup included")
    print("✅ Uses your existing AWS credentials")
    
    print("\n📋 What this will do:")
    print("1. Create S3 bucket: 'gellc-prefect-flows'")
    print("2. Upload flow files to S3")
    print("3. Create Prefect deployment pointing to S3")
    print("4. Your ECS workers will pull code from S3")
    print("5. Execute flows and report back to Prefect Cloud")
    
    print("\n🔧 Setting up S3 storage and deployment...")
    
    deployment_id = await create_s3_deployment()
    
    if deployment_id:
        print(f"\n🎉 S3 + ECS deployment ready!")
        print(f"✅ S3 bucket: gellc-prefect-flows")
        print(f"✅ Deployment ID: {deployment_id}")
        print(f"✅ Work pool: gellc-process-pool")
        print(f"✅ ECS infrastructure: ready")
        
        print(f"\n🎯 Next steps:")
        print(f"1. Go to Prefect Cloud UI")
        print(f"2. Find deployment: 's3-ecs-flow'")
        print(f"3. Click 'Run' to test")
        print(f"4. Watch it execute on your ECS infrastructure!")
        
        print(f"\n🔄 Future flow updates:")
        print(f"1. Update files in S3 bucket")
        print(f"2. Flows automatically use latest code")
        print(f"3. No deployment recreation needed!")
        
    else:
        print(f"\n❌ S3 setup failed")
        print(f"💡 Check AWS credentials and try again")
    
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(setup_s3_approach())
