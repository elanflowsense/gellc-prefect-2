#!/usr/bin/env python3
"""
Create a deployment manually without storage dependencies
"""
import asyncio
from prefect import get_client
from prefect.client.schemas.objects import FlowRun
from prefect.client.schemas.actions import DeploymentCreate, FlowCreate
from prefect.client.schemas.objects import Flow

async def create_manual_deployment():
    """Create a deployment manually via API"""
    
    print("🔧 Creating deployment manually via API...")
    
    async with get_client() as client:
        
        # First, let's create a simple flow definition
        flow_code = '''
from prefect import flow, task

@task
def manual_task():
    print("🎉 Manual task running on ECS!")
    print("✅ This confirms ECS infrastructure works!")
    return "MANUAL_SUCCESS"

@flow
def manual_flow():
    print("🚀 Manual flow starting...")
    result = manual_task()
    print(f"📊 Result: {result}")
    return result

if __name__ == "__main__":
    manual_flow()
'''
        
        # Create the deployment directly
        deployment_data = DeploymentCreate(
            name="manual-ecs-test",
            flow_name="manual_flow",
            work_pool_name="gellc-process-pool",
            description="Manual deployment test",
            version="1.0.0",
            tags=["manual", "test"],
            # No storage - this should work with code in the container
            entrypoint="create_working_deployment.py:hello_ecs_flow",  # Reference existing file
            path=".",
        )
        
        try:
            deployment = await client.create_deployment(deployment=deployment_data)
            print(f"✅ Manual deployment created: {deployment.id}")
            
            # Test it
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=deployment.id
            )
            
            print(f"🎯 Flow run created: {flow_run.id}")
            
            # Monitor
            for i in range(20):
                updated_flow_run = await client.read_flow_run(flow_run.id)
                state = updated_flow_run.state.type
                message = updated_flow_run.state.message or 'No message'
                
                print(f"[{i*5:2d}s] {state:12} | {message}")
                
                if state == "COMPLETED":
                    print(f"\n🎉 SUCCESS! Manual deployment works!")
                    return True
                elif state in ["FAILED", "CRASHED"]:
                    print(f"\n❌ Failed: {message}")
                    return False
                
                await asyncio.sleep(5)
            
            return False
            
        except Exception as e:
            print(f"❌ Error creating manual deployment: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = asyncio.run(create_manual_deployment())
    if success:
        print("\n🎉 Manual deployment approach works!")
    else:
        print("\n❌ Manual deployment failed")
