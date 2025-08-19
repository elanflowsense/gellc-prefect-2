#!/usr/bin/env python3
"""
Test with an embedded flow (no external file dependencies)
"""
import asyncio
from prefect import flow, task, get_client

@task
def say_hello_task(name: str = "ECS"):
    """Simple task that prints hello"""
    message = f"Hello, {name}! This is running on ECS! 🚀"
    print(message)
    return message

@flow(name="embedded-hello-flow")
def embedded_hello_flow(name: str = "ECS"):
    """Simple embedded flow for testing"""
    print("🚀 Starting embedded flow on ECS...")
    result = say_hello_task(name)
    print(f"✅ Flow completed with result: {result}")
    return result

async def test_embedded_flow():
    """Test running the embedded flow directly"""
    
    print("🧪 Testing embedded flow...")
    
    # Just run the flow directly to test
    print("Running flow locally first...")
    local_result = embedded_hello_flow("Local Test")
    print(f"Local result: {local_result}")
    
    # Now create a minimal deployment
    print("\n🚀 Creating deployment...")
    
    async with get_client() as client:
        # Create the flow run directly without deployment first
        flow_run = await client.create_flow_run(
            flow=embedded_hello_flow,
            name="direct-ecs-test",
            parameters={"name": "Direct ECS"}
        )
        
        print(f"🎯 Created direct flow run: {flow_run.id}")
        print(f"📋 Flow run name: {flow_run.name}")
        
        # Monitor the run
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
    flow_run = asyncio.run(test_embedded_flow())
    print(f"\n🔗 View in Prefect Cloud:")
    print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
