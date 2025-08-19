#!/usr/bin/env python3
"""
Simple approach: Store code in git, let Prefect pull it
"""
import asyncio
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect import get_client

async def create_git_deployment():
    """Create deployment that pulls code from git"""
    
    print("🚀 Creating deployment with git storage...")
    
    # If your code is in a git repo, use this approach
    github_storage = GitHub(
        repository="https://github.com/your-org/your-repo.git",  # Replace with your repo
        reference="main"  # or your branch
    )
    
    deployment = await Deployment.build_from_flow(
        flow="flows/your_flow.py:your_flow",  # Path in your git repo
        name="GIT-code-deployment", 
        work_pool_name="gellc-process-pool",
        storage=github_storage,
        tags=["git", "clean", "modern"],
        description="Flow code from git repository",
        version="1.0.0"
    )
    
    deployment_id = await deployment.apply()
    print(f"✅ Deployment created: {deployment_id}")
    print(f"✅ Code source: Git repository")
    
    return deployment_id

# Uncomment to use:
# if __name__ == "__main__":
#     asyncio.run(create_git_deployment())
