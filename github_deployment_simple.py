#!/usr/bin/env python3
"""
Simple GitHub deployment - cleanest approach for ECS
"""
import asyncio
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect import get_client
from app_flow import app_flow

async def create_github_deployment():
    """Create deployment that pulls code from GitHub"""
    
    print("🚀 Creating GitHub deployment...")
    print("=" * 40)
    
    # TODO: Replace with your actual GitHub repository
    # github_storage = GitHub(
    #     repository="https://github.com/YOUR_USERNAME/gellc-prefect-2.git",
    #     reference="main"
    # )
    
    # For now, let's create it without storage and see what happens
    deployment = await Deployment.build_from_flow(
        flow=app_flow,
        name="GITHUB-test-deployment",
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        entrypoint="app_flow.py:app_flow",  # File path in the repo
        # storage=github_storage,  # Will add this once you have GitHub repo
        tags=["github", "test", "simple"],
        description="Test deployment for GitHub approach",
        version="1.0.0"
    )
    
    deployment_id = await deployment.apply()
    
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"📁 Entry point: app_flow.py:app_flow")
    print(f"🔗 Work pool: gellc-process-pool")
    
    # Test it
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "GITHUB TEST"}
        )
        
        print(f"\n🎯 Test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 Test Flow Run URL:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"{base_url}/flow-runs/flow-run/{flow_run.id}")
        
    return deployment_id

if __name__ == "__main__":
    asyncio.run(create_github_deployment())
