#!/usr/bin/env python3
"""
Create a simple deployment to debug what's available in the process worker environment
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect import get_client

@task
def debug_environment_task():
    """Debug what's available in the worker environment"""
    import sys
    import pkg_resources
    
    print("🔍 DEBUGGING WORKER ENVIRONMENT")
    print("=" * 50)
    
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Python executable: {sys.executable}")
    print(f"📦 Python path: {sys.path}")
    
    print("\n📋 INSTALLED PACKAGES:")
    try:
        installed_packages = [d.project_name for d in pkg_resources.working_set]
        for package in sorted(installed_packages):
            if any(keyword in package.lower() for keyword in ['prefect', 'aws', 's3', 'boto']):
                try:
                    version = pkg_resources.get_distribution(package).version
                    print(f"  ✅ {package}: {version}")
                except:
                    print(f"  ⚠️ {package}: version unknown")
    except Exception as e:
        print(f"❌ Error listing packages: {e}")
    
    print("\n🔍 CHECKING PREFECT BLOCKS:")
    try:
        from prefect.blocks.core import Block
        available_blocks = Block.get_block_class_for_key.__globals__.get('registry', {})
        print(f"Available block types: {list(available_blocks.keys())}")
    except Exception as e:
        print(f"❌ Error checking blocks: {e}")
    
    print("\n🔍 CHECKING S3 AVAILABILITY:")
    try:
        from prefect.filesystems import S3
        print("✅ prefect.filesystems.S3 is available")
    except ImportError as e:
        print(f"❌ prefect.filesystems.S3 not available: {e}")
    
    try:
        from prefect_aws import S3Bucket
        print("✅ prefect_aws.S3Bucket is available")
    except ImportError as e:
        print(f"❌ prefect_aws.S3Bucket not available: {e}")
    
    print("\n🔍 ENVIRONMENT VARIABLES:")
    import os
    for key in ['PREFECT_API_URL', 'PREFECT_API_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
        value = os.environ.get(key, 'NOT SET')
        if 'KEY' in key and value != 'NOT SET':
            value = value[:10] + "..." if len(value) > 10 else value
        print(f"  {key}: {value}")
    
    return "Environment debug completed"

@flow
def debug_environment_flow():
    """Flow to debug the worker environment"""
    print("🚀 Starting environment debug flow...")
    result = debug_environment_task()
    print(f"✅ Debug result: {result}")
    return result

async def create_debug_deployment():
    """Create a simple debug deployment"""
    
    print("🔍 Creating debug deployment...")
    print("=" * 40)
    
    # Create deployment with process pool (no storage to avoid any block issues)
    deployment = await Deployment.build_from_flow(
        flow=debug_environment_flow,
        name="DEBUG-worker-environment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",
        # No storage parameter = local storage, no blocks needed
        entrypoint="debug_environment_flow.py:debug_environment_flow",
        description="Debug deployment to check worker environment",
        version="1.0.0",
        tags=["DEBUG", "environment", "worker"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n📋 Debug deployment created!")
    print(f"✅ Deployment ID: {deployment_id}")
    
    # Create debug flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id
        )
        
        print(f"\n🎯 Debug flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"\n🔗 Debug Flow Run URL:")
        print(f"{base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 Check the logs to see what's available in your worker environment!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_debug_deployment())
