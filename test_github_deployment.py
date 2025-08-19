#!/usr/bin/env python3
"""
Test the GitHub deployment with new flow run
"""
import asyncio
from prefect import get_client

async def test_github_deployment():
    """Test the GitHub deployment by creating a new flow run"""
    
    print("🧪 Testing GitHub deployment...")
    
    # The deployment ID from our previous GitHub deployment
    deployment_id = "bbc5f4d4-bff8-4511-9144-b6777974e738"
    
    async with get_client() as client:
        # Create a new flow run
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "GITHUB TEST WITH GIT"}
        )
        
        print(f"🎯 New GitHub test flow run created:")
        print(f"✅ Flow Run ID: {flow_run.id}")
        print(f"✅ Flow Run Name: {flow_run.name}")
        print(f"✅ Deployment: GITHUB-deployment")
        print(f"✅ Code Source: elanflowsense/gellc-prefect-2 on GitHub")
        
        print(f"\n🔗 Test this flow run:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"{base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n💡 This should work now that ECS containers have Git installed!")
        print(f"🐳 Containers will clone your GitHub repo and run app_flow.py")
        
    return flow_run.id

if __name__ == "__main__":
    flow_run_id = asyncio.run(test_github_deployment())
