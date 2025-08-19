#!/usr/bin/env python3
"""
Create deployment that pulls code from GitHub repository
"""
import asyncio
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect import get_client
from app_flow import app_flow

async def create_github_deployment():
    """Create deployment using GitHub storage"""
    
    print("🚀 Creating GitHub deployment...")
    print("=" * 50)
    
    # Create GitHub storage pointing to your repository
    github_storage = GitHub(
        repository="https://github.com/elanflowsense/gellc-prefect-2.git",
        reference="main"  # or "master" depending on your default branch
    )
    
    print("📁 GitHub repository: elanflowsense/gellc-prefect-2")
    print("🌿 Branch: main")
    
    # Create deployment
    deployment = await Deployment.build_from_flow(
        flow=app_flow,
        name="GITHUB-deployment",
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        storage=github_storage,
        entrypoint="app_flow.py:app_flow",  # Path to flow in your repo
        tags=["github", "production", "working"],
        description="Deployment pulling code from GitHub repository",
        version="1.0.0"
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 GITHUB DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: GITHUB-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Code Source: GitHub (elanflowsense/gellc-prefect-2)")
    print(f"✅ Entry Point: app_flow.py:app_flow")
    print(f"✅ Work Pool: gellc-process-pool")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "GITHUB TEST"}
        )
        
        print(f"\n🎯 GitHub test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 GITHUB DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS PULLS CODE FROM GITHUB ON EACH RUN!")
        print(f"💡 ECS containers will clone your repo and run the flow!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_github_deployment())
