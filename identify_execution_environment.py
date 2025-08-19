#!/usr/bin/env python3
"""
Deploy a flow that will tell us exactly where the process workers are running
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect import get_client

@task
def identify_execution_environment():
    """Identify where this task is actually executing"""
    import sys
    import os
    import platform
    import socket
    
    print("🔍 EXECUTION ENVIRONMENT IDENTIFICATION")
    print("=" * 50)
    
    # Basic system info
    print(f"🖥️  SYSTEM INFO:")
    print(f"  Platform: {platform.platform()}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")
    print(f"  Python: {sys.version}")
    
    # Network info
    print(f"\n🌐 NETWORK INFO:")
    try:
        hostname = socket.gethostname()
        print(f"  Hostname: {hostname}")
        
        # Try to get IP
        try:
            ip = socket.gethostbyname(hostname)
            print(f"  IP Address: {ip}")
        except:
            print(f"  IP Address: Could not resolve")
            
        # Check if we're in AWS
        try:
            import urllib.request
            # Try AWS metadata service (ECS/EC2)
            req = urllib.request.Request('http://169.254.169.254/latest/meta-data/instance-id', 
                                       headers={'User-Agent': 'prefect-debug'})
            urllib.request.urlopen(req, timeout=2)
            print(f"  🎯 RUNNING ON AWS! (EC2/ECS)")
            
            # Get more AWS metadata
            try:
                req = urllib.request.Request('http://169.254.169.254/latest/meta-data/placement/availability-zone')
                with urllib.request.urlopen(req, timeout=2) as response:
                    az = response.read().decode()
                print(f"  AWS AZ: {az}")
            except:
                pass
                
            # Check if ECS
            try:
                if 'ECS_CONTAINER_METADATA_URI' in os.environ:
                    print(f"  🐳 RUNNING IN ECS CONTAINER!")
                    print(f"  ECS Metadata URI: {os.environ['ECS_CONTAINER_METADATA_URI']}")
            except:
                pass
                
        except:
            print(f"  Not running on AWS (no metadata service)")
            
    except Exception as e:
        print(f"  Error getting network info: {e}")
    
    # Environment variables
    print(f"\n🔧 RELEVANT ENVIRONMENT VARIABLES:")
    relevant_env = ['HOME', 'USER', 'PATH', 'PWD', 'HOSTNAME', 'AWS_REGION', 
                   'AWS_DEFAULT_REGION', 'ECS_CONTAINER_METADATA_URI', 'ECS_CONTAINER_METADATA_URI_V4',
                   'PREFECT_API_URL', 'PREFECT_API_KEY']
    
    for var in relevant_env:
        value = os.environ.get(var, 'NOT SET')
        if 'KEY' in var and value != 'NOT SET':
            value = value[:10] + "..." if len(value) > 10 else value
        print(f"  {var}: {value}")
    
    # Check for containerization signs
    print(f"\n🐳 CONTAINERIZATION SIGNS:")
    container_signs = [
        ('/proc/1/cgroup', 'docker' in open('/proc/1/cgroup').read() if os.path.exists('/proc/1/cgroup') else False),
        ('/.dockerenv', os.path.exists('/.dockerenv')),
        ('/proc/self/mountinfo', 'docker' in open('/proc/self/mountinfo').read() if os.path.exists('/proc/self/mountinfo') else False)
    ]
    
    for sign, exists in container_signs:
        print(f"  {sign}: {'✅ YES' if exists else '❌ NO'}")
    
    # Current working directory and filesystem
    print(f"\n📁 FILESYSTEM INFO:")
    print(f"  Current working directory: {os.getcwd()}")
    print(f"  Home directory: {os.path.expanduser('~')}")
    
    # Check Python packages
    print(f"\n📦 PYTHON PACKAGES (S3 related):")
    try:
        import pkg_resources
        s3_packages = ['prefect-aws', 'boto3', 's3fs', 'botocore']
        for package in s3_packages:
            try:
                version = pkg_resources.get_distribution(package).version
                print(f"  ✅ {package}: {version}")
            except pkg_resources.DistributionNotFound:
                print(f"  ❌ {package}: NOT INSTALLED")
    except Exception as e:
        print(f"  Error checking packages: {e}")
    
    return f"Environment identified: {platform.platform()}"

@flow
def identify_environment_flow():
    """Flow to identify execution environment"""
    print("🚀 Starting environment identification...")
    result = identify_execution_environment()
    print(f"✅ Identification complete: {result}")
    return result

async def deploy_environment_identifier():
    """Deploy the environment identification flow"""
    
    print("🚀 Deploying environment identifier...")
    print("=" * 40)
    
    # Create simple deployment (no storage blocks)
    deployment = await Deployment.build_from_flow(
        flow=identify_environment_flow,
        name="IDENTIFY-worker-environment",
        work_queue_name="default",  
        work_pool_name="gellc-process-pool",
        # No storage = local, should work
        entrypoint="identify_environment_flow.py:identify_environment_flow",
        description="Identify where process workers are executing",
        version="1.0.0",
        tags=["IDENTIFY", "environment", "location"]
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n📋 Environment identifier deployed!")
    print(f"✅ Deployment ID: {deployment_id}")
    
    # Create and run immediately
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(deployment_id=deployment_id)
        
        print(f"\n🎯 Environment identification running:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"\n🔗 Check results here:")
        print(f"{base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 This will tell us EXACTLY where your workers are running!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(deploy_environment_identifier())
