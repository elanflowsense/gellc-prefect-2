#!/usr/bin/env python3
"""
Create deployment using modern GitHub storage from prefect-github
"""
import asyncio
from prefect.deployments import Deployment
from prefect import get_client
from app_flow import app_flow

async def create_modern_github_deployment():
    """Create deployment using modern GitHub storage"""
    
    print("🚀 Creating modern GitHub deployment...")
    print("=" * 60)
    
    try:
        from prefect_github import GitHubRepository
        print("✅ Using modern GitHubRepository from prefect-github")
        
        # Create GitHub storage using modern prefect-github
        github_storage = GitHubRepository(
            repository_url="https://github.com/elanflowsense/gellc-prefect-2.git",
            reference="main"
        )
        
    except ImportError:
        print("⚠️ prefect-github not available, using deprecated GitHub")
        from prefect.filesystems import GitHub
        
        github_storage = GitHub(
            repository="https://github.com/elanflowsense/gellc-prefect-2.git",
            reference="main"
        )
    
    print("📁 GitHub repository: elanflowsense/gellc-prefect-2")
    print("🌿 Branch: main")
    
    # Delete any existing deployment with same name
    async with get_client() as client:
        try:
            deployments = await client.read_deployments()
            for dep in deployments:
                if dep.name == "MODERN-github-deployment":
                    print(f"🗑️ Deleting existing deployment: {dep.id}")
                    await client.delete_deployment(dep.id)
        except Exception as e:
            print(f"⚠️ Error cleaning up: {e}")
    
    # Create deployment
    deployment = await Deployment.build_from_flow(
        flow=app_flow,
        name="MODERN-github-deployment",
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        storage=github_storage,
        entrypoint="app_flow.py:app_flow",  # Path to flow in your repo
        tags=["modern", "github", "working", "fixed"],
        description="Modern deployment using updated GitHub storage",
        version="2.0.0"
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 MODERN GITHUB DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: MODERN-github-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"✅ Code Source: GitHub (elanflowsense/gellc-prefect-2)")
    print(f"✅ Entry Point: app_flow.py:app_flow")
    print(f"✅ Work Pool: gellc-process-pool")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "MODERN GITHUB TEST"}
        )
        
        print(f"\n🎯 Modern GitHub test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 MODERN GITHUB DEPLOYMENT URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🎉 THIS USES MODERN GITHUB STORAGE!")
        print(f"💡 Should work with Prefect 2.20+ and prefect-github!")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_modern_github_deployment())
