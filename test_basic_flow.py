#!/usr/bin/env python3
"""
Test a basic flow that should work in our ECS environment
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment

@task
def simple_task():
    print("🎉 Hello from ECS!")
    print("✅ This task is running successfully!")
    return "success"

@flow
def test_ecs_flow():
    """A simple flow to test ECS execution"""
    print("🚀 Starting ECS test flow...")
    result = simple_task()
    print(f"📊 Task result: {result}")
    print("🏁 ECS test flow completed!")
    return result

async def create_and_test_deployment():
    """Create a deployment and test it"""
    
    print("🚀 Creating test deployment...")
    
    # Create deployment
    deployment = await Deployment.build_from_flow(
        flow=test_ecs_flow,
        name="test-ecs-flow",
        work_pool_name="gellc-process-pool",
        description="Simple test flow for ECS",
        version="1.0.0",
        tags=["test", "ecs"]
    )
    
    deployment_id = await deployment.apply()
    print(f"✅ Deployment created: {deployment_id}")
    
    # Test the deployment
    from prefect import get_client
    
    async with get_client() as client:
        # Create a flow run
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id
        )
        
        print(f"🎯 Created flow run: {flow_run.id}")
        print(f"📋 Flow run name: {flow_run.name}")
        
        # Monitor for 1 minute
        for i in range(12):
            updated_flow_run = await client.read_flow_run(flow_run.id)
            print(f"[{i*5:2d}s] State: {updated_flow_run.state.type:10} | Message: {updated_flow_run.state.message or 'No message'}")
            
            if updated_flow_run.state.type in ["COMPLETED", "FAILED", "CRASHED"]:
                print(f"\n📊 Final state: {updated_flow_run.state.type}")
                if updated_flow_run.state.type == "COMPLETED":
                    print("🎉 SUCCESS! Flow executed successfully on ECS!")
                else:
                    print(f"❌ Flow failed: {updated_flow_run.state.message}")
                break
            
            await asyncio.sleep(5)
        
        return flow_run

if __name__ == "__main__":
    flow_run = asyncio.run(create_and_test_deployment())
    print(f"\n🔗 View in Prefect Cloud:")
    print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
