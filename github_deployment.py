#!/usr/bin/env python3
"""
Create a deployment using GitHub storage
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

@task
def github_task(name: str = "GitHub"):
    """Task that will run from GitHub"""
    print(f"🎉 Hello from {name}!")
    print("✅ This flow is running from GitHub on ECS!")
    print("🚀 GitHub + ECS + Prefect Cloud = Success!")
    return f"SUCCESS from {name}"

@flow
def github_flow(name: str = "GitHub ECS"):
    """Flow that will be stored in GitHub"""
    print(f"🚀 Starting GitHub flow for: {name}")
    result = github_task(name)
    print(f"📊 Flow result: {result}")
    return result

async def create_github_deployment():
    """Create a deployment using GitHub storage"""
    
    print("🐙 Creating GitHub-based deployment...")
    
    # You'll need to provide:
    # 1. Your GitHub repository
    # 2. Your GitHub access token (for private repos)
    
    print("📋 To use GitHub storage, you need:")
    print("1. A GitHub repository with your flow files")
    print("2. A GitHub personal access token (for private repos)")
    print("3. The repository should contain your flow files")
    
    # Example configuration (you'll need to customize this)
    github_storage = GitHub(
        repository="your-username/your-repo-name",  # Change this
        reference="main",  # or your branch name
        # access_token="your-github-token",  # Uncomment and add your token for private repos
    )
    
    try:
        deployment = await Deployment.build_from_flow(
            flow=github_flow,
            name="github-ecs-flow",
            work_pool_name="gellc-process-pool",
            storage=github_storage,
            entrypoint="flows/github_flow.py:github_flow",  # Path to your flow in the repo
            description="Flow running from GitHub on ECS",
            version="1.0.0",
            tags=["github", "ecs", "production"]
        )
        
        deployment_id = await deployment.apply()
        print(f"✅ GitHub deployment created: {deployment_id}")
        
        return deployment_id
        
    except Exception as e:
        print(f"❌ Error creating GitHub deployment: {e}")
        print("\n💡 This is expected - you need to set up the GitHub repository first!")
        return None

async def setup_github_approach():
    """Show how to set up GitHub approach"""
    
    print("🐙 GitHub + ECS Deployment Setup")
    print("=" * 50)
    
    print("\n📋 Steps to set up GitHub storage:")
    print("1. Create a GitHub repository (can be private)")
    print("2. Create a folder structure like:")
    print("   your-repo/")
    print("   ├── flows/")
    print("   │   ├── __init__.py")
    print("   │   └── github_flow.py")
    print("   └── requirements.txt")
    
    print("\n📄 Example github_flow.py content:")
    print('''
from prefect import flow, task

@task
def hello_task(name: str = "ECS"):
    print(f"🎉 Hello {name} from GitHub!")
    return f"Hello {name}!"

@flow
def hello_flow(name: str = "ECS"):
    print("🚀 Flow starting from GitHub...")
    result = hello_task(name)
    print(f"✅ Flow completed: {result}")
    return result
''')
    
    print("\n🔑 For private repositories:")
    print("1. Go to GitHub Settings > Developer settings > Personal access tokens")
    print("2. Create a token with 'repo' permissions")
    print("3. Use it in the GitHub storage configuration")
    
    print("\n🚀 Advantages of GitHub approach:")
    print("✅ No file path issues")
    print("✅ Version control for flows") 
    print("✅ Easy updates without rebuilding containers")
    print("✅ Team collaboration")
    print("✅ Multiple flows in one repository")
    
    print("\n📦 Your ECS infrastructure will:")
    print("✅ Pull flow code from GitHub at runtime")
    print("✅ Execute flows in ECS containers")
    print("✅ Send results back to Prefect Cloud")
    
    # Show example with public repo
    print("\n🧪 Testing with a public repository...")
    
    return await create_github_deployment()

if __name__ == "__main__":
    deployment_id = asyncio.run(setup_github_approach())
    
    if deployment_id:
        print(f"\n🎉 GitHub deployment ready!")
    else:
        print(f"\n💡 Set up your GitHub repository and try again!")
        print(f"\nOnce you have a GitHub repo with flows:")
        print(f"1. Update the repository name in this script")
        print(f"2. Add your access token if needed")
        print(f"3. Run this script again")
        print(f"4. Your flows will run from GitHub on ECS! 🚀")
