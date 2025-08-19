#!/usr/bin/env python3
"""
Create Prefect deployment with S3 storage
"""
import asyncio
from prefect.deployments import Deployment
from prefect.filesystems import S3
from my_prefect_flow import my_first_flow

# Configuration
DEPLOYMENT_NAME = "my-first-flow-s3"
WORK_POOL_NAME = "gellc-ecs-pool"  # Use your existing ECS work pool
S3_STORAGE_BLOCK = "gellc-s3-storage"

async def create_s3_deployment():
    """Create deployment with S3 storage"""
    
    print("🚀 Creating Prefect deployment with S3 storage...")
    print("=" * 60)
    
    try:
        # Load S3 storage block
        s3_storage = await S3.load(S3_STORAGE_BLOCK)
        print(f"✅ Loaded S3 storage block: {S3_STORAGE_BLOCK}")
        
        # Create deployment
        deployment = await Deployment.build_from_flow(
            flow=my_first_flow,
            name=DEPLOYMENT_NAME,
            work_pool_name=WORK_POOL_NAME,
            storage=s3_storage,
            description="GELLC Prefect flow with S3 code storage",
            version="2.0.0",
            tags=["ecs", "gellc", "s3", "production"],
            # Set the path where the flow code is located in S3
            path=".",  # Root of the uploaded zip
            entrypoint="my_prefect_flow.py:my_first_flow"
        )
        
        # Apply the deployment
        deployment_id = await deployment.apply()
        
        print(f"\n🎉 Deployment Created Successfully!")
        print("=" * 50)
        print(f"📊 Deployment Details:")
        print(f"  Name: {DEPLOYMENT_NAME}")
        print(f"  ID: {deployment_id}")
        print(f"  Work Pool: {WORK_POOL_NAME}")
        print(f"  Storage: S3 ({s3_storage.bucket_path})")
        print(f"  Version: 2.0.0")
        print(f"  Tags: ecs, gellc, s3, production")
        
        print(f"\n🔧 Next Steps:")
        print(f"1. Test the deployment:")
        print(f"   python test_s3_deployment.py")
        print(f"")
        print(f"2. Run the deployment manually:")
        print(f"   prefect deployment run '{my_first_flow.name}/{DEPLOYMENT_NAME}'")
        print(f"")
        print(f"3. Start a worker (if not running):")
        print(f"   prefect worker start --pool {WORK_POOL_NAME}")
        print(f"")
        print(f"4. Monitor in Prefect Cloud:")
        print(f"   https://app.prefect.cloud/")
        
        return deployment_id
        
    except Exception as e:
        print(f"❌ Failed to create deployment: {e}")
        import traceback
        traceback.print_exc()
        return None

async def verify_deployment(deployment_id):
    """Verify the deployment was created correctly"""
    
    if not deployment_id:
        return False
    
    print(f"\n🔍 Verifying deployment...")
    
    try:
        from prefect import get_client
        
        async with get_client() as client:
            # Get deployment details
            deployment = await client.read_deployment(deployment_id)
            
            print(f"✅ Deployment verified:")
            print(f"  Name: {deployment.name}")
            print(f"  Flow Name: {deployment.flow_name}")
            print(f"  Work Pool: {deployment.work_pool_name}")
            print(f"  Storage Type: {type(deployment.storage).__name__}")
            
            return True
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

async def main():
    """Main function"""
    
    print("🚀 Setting up S3-based Prefect deployment")
    print("=" * 60)
    
    # Check if S3 storage block exists
    try:
        await S3.load(S3_STORAGE_BLOCK)
        print(f"✅ S3 storage block '{S3_STORAGE_BLOCK}' found")
    except Exception as e:
        print(f"❌ S3 storage block not found: {e}")
        print("Please run:")
        print("1. python setup_s3_storage.py")
        print("2. python upload_code_to_s3.py")
        return
    
    # Create deployment
    deployment_id = await create_s3_deployment()
    
    # Verify deployment
    if deployment_id:
        await verify_deployment(deployment_id)

if __name__ == "__main__":
    asyncio.run(main())
