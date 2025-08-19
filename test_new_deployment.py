#!/usr/bin/env python3
"""
Test the new deployment
"""
import asyncio
import time
from prefect import get_client

async def test_new_deployment():
    """Test the new deployment"""
    
    print("🚀 Testing new deployment...")
    
    try:
        async with get_client() as client:
            # Get the new deployment
            deployments = await client.read_deployments()
            target_deployment = None
            
            for deployment in deployments:
                if deployment.name == "my-first-flow-process":
                    target_deployment = deployment
                    break
            
            if not target_deployment:
                print("❌ Deployment 'my-first-flow-process' not found")
                return
            
            print(f"✅ Found deployment: {target_deployment.name}")
            print(f"🏊 Work Pool: {target_deployment.work_pool_name}")
            
            # Create a flow run
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=target_deployment.id
            )
            
            print(f"\n🎯 Created flow run: {flow_run.id}")
            print(f"📋 Flow run name: {flow_run.name}")
            print(f"🔄 Initial state: {flow_run.state.type}")
            
            # Monitor the flow run
            print(f"\n👀 Monitoring flow run...")
            
            for i in range(12):  # Monitor for 1 minute
                updated_flow_run = await client.read_flow_run(flow_run.id)
                
                print(f"[{i*5:2d}s] State: {updated_flow_run.state.type:10} | Message: {updated_flow_run.state.message or 'No message'}")
                
                if updated_flow_run.state.type in ["COMPLETED", "FAILED", "CRASHED"]:
                    print(f"\n📊 Final state: {updated_flow_run.state.type}")
                    break
                
                await asyncio.sleep(5)
            else:
                print(f"\n⏱️  Flow run still in progress...")
            
            return flow_run
            
    except Exception as e:
        print(f"❌ Error testing deployment: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    flow_run = asyncio.run(test_new_deployment())
    if flow_run:
        print(f"\n🔗 View in Prefect Cloud:")
        print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
    else:
        print("❌ Failed to test deployment")
