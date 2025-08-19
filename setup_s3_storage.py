#!/usr/bin/env python3
"""
Setup S3 storage for Prefect deployments
"""
import asyncio
import boto3
from prefect.filesystems import S3
from prefect.blocks.system import Secret
import os

# Configuration
AWS_REGION = "us-east-1"
BUCKET_NAME = "gellc-prefect-code-storage"
BUCKET_PREFIX = "flows/"

async def create_s3_bucket():
    """Create S3 bucket for code storage"""
    
    print(f"🪣 Creating S3 bucket: {BUCKET_NAME}")
    
    # Create S3 client
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"✅ Bucket {BUCKET_NAME} already exists")
    except:
        # Create bucket
        if AWS_REGION == 'us-east-1':
            # us-east-1 doesn't need LocationConstraint
            s3_client.create_bucket(Bucket=BUCKET_NAME)
        else:
            s3_client.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
            )
        print(f"✅ Created S3 bucket: {BUCKET_NAME}")
    
    # Set bucket policy for Prefect access
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PrefectCodeAccess",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole"
                },
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{BUCKET_NAME}",
                    f"arn:aws:s3:::{BUCKET_NAME}/*"
                ]
            }
        ]
    }
    
    try:
        import json
        s3_client.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=json.dumps(bucket_policy)
        )
        print("✅ Set bucket policy for ECS access")
    except Exception as e:
        print(f"⚠️  Warning: Could not set bucket policy: {e}")
    
    return BUCKET_NAME

async def create_s3_block():
    """Create Prefect S3 storage block"""
    
    print(f"📦 Creating Prefect S3 storage block...")
    
    # Create S3 filesystem block
    s3_block = S3(
        bucket_path=f"s3://{BUCKET_NAME}/{BUCKET_PREFIX}",
        aws_access_key_id=None,  # Use IAM role
        aws_secret_access_key=None,  # Use IAM role
        region_name=AWS_REGION
    )
    
    # Save the block
    await s3_block.save("gellc-s3-storage", overwrite=True)
    print("✅ S3 storage block saved as 'gellc-s3-storage'")
    
    return s3_block

async def test_s3_access():
    """Test S3 access"""
    
    print("🔍 Testing S3 access...")
    
    try:
        # Load the S3 block
        s3_block = await S3.load("gellc-s3-storage")
        
        # Test write
        test_content = "# Test file for Prefect S3 storage\nprint('Hello from S3!')\n"
        await s3_block.write_path("test_file.py", test_content.encode())
        print("✅ Successfully wrote test file to S3")
        
        # Test read
        content = await s3_block.read_path("test_file.py")
        print("✅ Successfully read test file from S3")
        
        # Clean up test file
        try:
            import boto3
            s3_client = boto3.client('s3', region_name=AWS_REGION)
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=f"{BUCKET_PREFIX}test_file.py")
            print("✅ Cleaned up test file")
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"❌ S3 access test failed: {e}")
        return False

def print_next_steps():
    """Print next steps"""
    
    print("\n🎉 S3 Storage Setup Complete!")
    print("=" * 50)
    print(f"📊 Configuration:")
    print(f"  S3 Bucket: {BUCKET_NAME}")
    print(f"  Bucket Path: s3://{BUCKET_NAME}/{BUCKET_PREFIX}")
    print(f"  Region: {AWS_REGION}")
    print(f"  Storage Block: gellc-s3-storage")
    print()
    print("🔧 Next Steps:")
    print("1. Upload your code to S3:")
    print("   python upload_code_to_s3.py")
    print()
    print("2. Create deployment with S3 storage:")
    print("   python create_s3_deployment.py")
    print()
    print("3. Run deployment:")
    print("   prefect deployment run 'my-first-flow/my-first-flow-s3'")

async def main():
    """Main setup function"""
    
    print("🚀 Setting up S3 storage for Prefect deployments")
    print("=" * 60)
    
    # Check AWS credentials
    try:
        boto3.client('sts').get_caller_identity()
        print("✅ AWS credentials configured")
    except Exception as e:
        print(f"❌ AWS credentials not configured: {e}")
        print("Please run: aws configure")
        return
    
    # Create S3 bucket
    bucket = await create_s3_bucket()
    
    # Create Prefect S3 block
    s3_block = await create_s3_block()
    
    # Test S3 access
    success = await test_s3_access()
    
    if success:
        print_next_steps()
    else:
        print("❌ Setup failed - please check AWS permissions")

if __name__ == "__main__":
    asyncio.run(main())
