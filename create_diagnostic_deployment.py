#!/usr/bin/env python3
"""
Diagnostic deployment to see what files the worker can actually access
"""
import asyncio
import os
import subprocess
from pathlib import Path
from prefect.deployments import Deployment
from prefect import get_client, flow, task

@task
def diagnostic_task():
    """Task that shows us what the worker can see"""
    print("🔍 WORKER DIAGNOSTIC INFORMATION")
    print("=" * 60)
    
    # Current working directory
    cwd = os.getcwd()
    print(f"📁 Current working directory: {cwd}")
    
    # List all files in current directory
    print(f"\n📋 Files in current directory ({cwd}):")
    try:
        files = os.listdir(cwd)
        for f in sorted(files):
            path = os.path.join(cwd, f)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                print(f"   📄 {f} ({size} bytes)")
            elif os.path.isdir(path):
                print(f"   📁 {f}/")
    except Exception as e:
        print(f"   ❌ Error listing files: {e}")
    
    # Look for Python files specifically
    print(f"\n🐍 Python files in current directory:")
    try:
        py_files = [f for f in os.listdir(cwd) if f.endswith('.py')]
        if py_files:
            for py_file in sorted(py_files):
                print(f"   ✅ {py_file}")
        else:
            print("   ❌ No Python files found!")
    except Exception as e:
        print(f"   ❌ Error finding Python files: {e}")
    
    # Check if specific files exist
    target_files = ['simple_ecs_flow.py', 'app_flow.py', 'my_prefect_flow.py']
    print(f"\n🎯 Checking for specific flow files:")
    for target_file in target_files:
        file_path = os.path.join(cwd, target_file)
        if os.path.exists(file_path):
            print(f"   ✅ {target_file} - EXISTS")
            try:
                with open(file_path, 'r') as f:
                    first_line = f.readline().strip()
                    print(f"      First line: {first_line}")
            except Exception as e:
                print(f"      ❌ Cannot read: {e}")
        else:
            print(f"   ❌ {target_file} - NOT FOUND")
    
    # Check environment variables
    print(f"\n🔧 Environment variables:")
    env_vars = ['HOME', 'USER', 'PATH', 'PYTHONPATH', 'PREFECT_API_URL']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"   {var}: {value}")
    
    # Try to run git commands to see if we're in a git repo
    print(f"\n🔗 Git repository information:")
    try:
        git_output = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, timeout=10)
        if git_output.returncode == 0:
            print(f"   ✅ In git repository")
            
            # Get current branch
            branch_output = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, timeout=5)
            if branch_output.returncode == 0:
                print(f"   📋 Current branch: {branch_output.stdout.strip()}")
            
            # Get remote URL
            remote_output = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                         capture_output=True, text=True, timeout=5)
            if remote_output.returncode == 0:
                print(f"   🔗 Remote URL: {remote_output.stdout.strip()}")
                
        else:
            print(f"   ❌ Not in git repository or git not available")
            print(f"   Error: {git_output.stderr}")
    except Exception as e:
        print(f"   ❌ Git command failed: {e}")
    
    # Check if we can import the flow we're looking for
    print(f"\n🏃 Testing imports:")
    try:
        import simple_ecs_flow
        print(f"   ✅ Can import simple_ecs_flow")
        print(f"   📍 Module file: {simple_ecs_flow.__file__}")
        
        # Try to get the flow function
        if hasattr(simple_ecs_flow, 'hello_flow'):
            print(f"   ✅ hello_flow function exists")
        else:
            print(f"   ❌ hello_flow function not found")
            print(f"   Available attributes: {dir(simple_ecs_flow)}")
            
    except ImportError as e:
        print(f"   ❌ Cannot import simple_ecs_flow: {e}")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
    
    print(f"\n✅ Diagnostic complete!")
    return {
        "working_directory": cwd,
        "files_found": len(os.listdir(cwd)) if os.path.exists(cwd) else 0,
        "python_files": [f for f in os.listdir(cwd) if f.endswith('.py')] if os.path.exists(cwd) else []
    }

@flow
def diagnostic_flow():
    """Diagnostic flow to understand worker environment"""
    print("🚀 Starting diagnostic flow...")
    print("🎯 This will show us what files the worker can access")
    
    result = diagnostic_task()
    
    print(f"\n📊 Diagnostic result: {result}")
    print("🏁 Diagnostic flow completed!")
    return result

async def create_diagnostic_deployment():
    """Create diagnostic deployment to see what worker can access"""
    
    print("🚀 Creating diagnostic deployment...")
    print("=" * 60)
    
    # Use same GitHub storage as before
    from prefect.filesystems import GitHub
    
    github_storage = GitHub(
        repository="https://github.com/elanflowsense/gellc-prefect-2.git",
        reference="main"
    )
    
    print("📁 GitHub repository: elanflowsense/gellc-prefect-2")
    print("🌿 Branch: main")
    print("🔍 This deployment will show us what the worker can see")
    
    # Delete any existing diagnostic deployment
    async with get_client() as client:
        try:
            deployments = await client.read_deployments()
            for dep in deployments:
                if dep.name == "DIAGNOSTIC-deployment":
                    print(f"🗑️ Deleting existing diagnostic deployment: {dep.id}")
                    await client.delete_deployment(dep.id)
        except Exception as e:
            print(f"⚠️ Error cleaning up: {e}")
    
    # Create diagnostic deployment with embedded flow
    deployment = await Deployment.build_from_flow(
        flow=diagnostic_flow,
        name="DIAGNOSTIC-deployment",
        work_pool_name="gellc-process-pool",
        work_queue_name="default",
        storage=github_storage,
        path=".",
        # Use this file's entrypoint since the flow is defined here
        entrypoint="create_diagnostic_deployment.py:diagnostic_flow",
        tags=["diagnostic", "debug", "investigation"],
        description="Diagnostic deployment to see what worker can access",
        version="1.0.0"
    )
    
    deployment_id = await deployment.apply()
    
    print(f"\n🎉 DIAGNOSTIC DEPLOYMENT CREATED!")
    print(f"✅ Deployment Name: DIAGNOSTIC-deployment")
    print(f"✅ Deployment ID: {deployment_id}")
    print(f"🔍 This will show us what files the worker can see")
    
    # Create test flow run
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id
        )
        
        print(f"\n🎯 Diagnostic flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        
        print(f"\n🔗 DIAGNOSTIC URLs:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"Deployment: {base_url}/deployments/deployment/{deployment_id}")
        print(f"Flow Run: {base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n🔍 CHECK THE FLOW RUN LOGS TO SEE:")
        print(f"   - What files the worker can see")
        print(f"   - What directory it's working in")
        print(f"   - Whether simple_ecs_flow.py is accessible")
        print(f"   - Git repository status")
        
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_diagnostic_deployment())
