#!/usr/bin/env python3
"""
Setup GitHub repository approach for Prefect flows
"""
import asyncio

def create_github_instructions():
    """Provide complete instructions for GitHub setup"""
    
    print("🐙 GITHUB + ECS SETUP INSTRUCTIONS")
    print("=" * 60)
    
    print("\n📋 Step 1: Create GitHub Repository")
    print("1. Go to GitHub.com")
    print("2. Create a new repository (public or private)")
    print("3. Name it something like 'gellc-prefect-flows'")
    
    print("\n📁 Step 2: Repository Structure")
    print("Create this folder structure in your repo:")
    print("""
gellc-prefect-flows/
├── flows/
│   ├── __init__.py                 # Empty file
│   ├── hello_flow.py              # Your test flow
│   ├── data_processing_flow.py     # Future flows
│   └── etl_flow.py                # Future flows
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation
""")
    
    print("\n📄 Step 3: Create flows/hello_flow.py")
    flow_content = '''from prefect import flow, task

@task
def hello_ecs_task(name: str = "ECS"):
    """Simple task for testing ECS execution"""
    message = f"🎉 Hello {name} from GitHub + ECS!"
    print(message)
    print("✅ This flow is running on ECS infrastructure!")
    print("🚀 Pulled from GitHub and executed on AWS ECS!")
    return message

@flow
def hello_ecs_flow(name: str = "ECS World"):
    """Simple flow for testing GitHub + ECS integration"""
    print(f"🚀 Starting GitHub flow for: {name}")
    print("📦 Code pulled from GitHub repository")
    print("🏗️ Executing on ECS infrastructure") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = hello_ecs_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 Flow completed successfully!")
    return result

if __name__ == "__main__":
    # Test the flow locally
    hello_ecs_flow("Local Test")
'''
    
    print("Copy this content to flows/hello_flow.py:")
    print("```python")
    print(flow_content)
    print("```")
    
    print("\n📄 Step 4: Create requirements.txt")
    print("Add this content to requirements.txt:")
    print("```")
    print("prefect>=2.0.0")
    print("```")
    
    print("\n🔑 Step 5: Create GitHub Token (for private repos)")
    print("1. Go to GitHub Settings > Developer settings > Personal access tokens")
    print("2. Generate new token (classic)")
    print("3. Select 'repo' permissions")
    print("4. Copy the token")
    
    print("\n🚀 Step 6: Create Deployment")
    deployment_code = '''import asyncio
from prefect.deployments import Deployment
from prefect_github import GitHubRepository

async def create_github_deployment():
    """Create deployment from GitHub"""
    
    # Configure GitHub storage
    github_repo = GitHubRepository(
        repository_url="https://github.com/YOUR-USERNAME/gellc-prefect-flows",
        reference="main",  # or your branch
        # For private repos, add:
        # access_token="your_github_token_here"
    )
    
    deployment = await Deployment.build_from_flow(
        flow_location="flows/hello_flow.py:hello_ecs_flow",
        storage=github_repo,
        name="github-ecs-flow",
        work_pool_name="gellc-process-pool",
        description="Flow from GitHub running on ECS",
        version="1.0.0",
        tags=["github", "ecs", "production"]
    )
    
    deployment_id = await deployment.apply()
    print(f"✅ Deployment created: {deployment_id}")
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_github_deployment())
    print(f"🎉 Ready to run from Prefect Cloud UI!")
'''
    
    print("Create this deployment script:")
    print("```python")
    print(deployment_code)
    print("```")
    
    print("\n🎯 Benefits of This Approach:")
    print("✅ Solves file path issues completely")
    print("✅ Version control for all your flows")
    print("✅ Easy updates (just push to GitHub)")
    print("✅ Team collaboration")
    print("✅ No container rebuilds needed")
    print("✅ Multiple flows in one repository")
    print("✅ Works with both public and private repos")
    
    print("\n🔄 Workflow:")
    print("1. Push flow changes to GitHub")
    print("2. Trigger flow from Prefect Cloud UI")
    print("3. ECS pulls latest code from GitHub")
    print("4. ECS executes flow")
    print("5. Results appear in Prefect Cloud")
    
    print("\n🎉 Once set up, you can:")
    print("✅ Run flows from Prefect Cloud UI")
    print("✅ Add new flows without infrastructure changes") 
    print("✅ Update flows by pushing to GitHub")
    print("✅ Scale ECS workers as needed")
    
    return True

def check_github_requirements():
    """Check if GitHub integration is available"""
    
    try:
        from prefect_github import GitHubRepository
        print("✅ prefect-github is available")
        return True
    except ImportError:
        print("❌ prefect-github not installed")
        print("📦 Install it with: pip install prefect-github")
        return False

if __name__ == "__main__":
    print("🔍 Checking requirements...")
    
    if check_github_requirements():
        print("\n✅ Ready for GitHub integration!")
    else:
        print("\n📦 Installing prefect-github...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "prefect-github"])
        print("✅ prefect-github installed!")
    
    print("\n" + "="*60)
    create_github_instructions()
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Create your GitHub repository")
    print(f"2. Add the flow files shown above")
    print(f"3. Create the deployment script")
    print(f"4. Run the deployment")
    print(f"5. Test from Prefect Cloud UI!")
    print(f"\n🚀 This will solve all the file path issues we've been having!")
