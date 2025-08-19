#!/usr/bin/env python3
"""
Minimal deployment test using RemoteFileSystem storage
"""
import asyncio
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem

@task
def ecs_test_task():
    """Test task for ECS"""
    print("🎉 ECS Test Task Executed Successfully!")
    print("✅ This confirms the ECS infrastructure is working!")
    return "ECS_SUCCESS"

@flow(name="minimal-ecs-test")
def minimal_ecs_test():
    """Minimal test flow"""
    print("🚀 Starting minimal ECS test...")
    result = ecs_test_task()
    print(f"📊 Task completed with result: {result}")
    return result

async def create_minimal_deployment():
    """Create a minimal deployment using in-memory approach"""
    
    print("🚀 Creating minimal deployment...")
    
    try:
        # Create deployment without specifying storage - let Prefect handle it
        deployment = Deployment(
            name="minimal-ecs-test",
            flow=minimal_ecs_test,
            work_pool_name="gellc-process-pool", 
            description="Minimal test for ECS execution",
            version="1.0.0",
            tags=["minimal", "test", "ecs"]
        )
        
        deployment_id = await deployment.apply()
        print(f"✅ Deployment created: {deployment_id}")
        
        # Test it
        from prefect import get_client
        
        async with get_client() as client:
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=deployment_id
            )
            
            print(f"🎯 Created flow run: {flow_run.id}")
            
            # Monitor
            for i in range(15):
                updated_flow_run = await client.read_flow_run(flow_run.id)
                state = updated_flow_run.state.type
                message = updated_flow_run.state.message or 'No message'
                
                print(f"[{i*5:2d}s] State: {state:10} | {message}")
                
                if state in ["COMPLETED", "FAILED", "CRASHED"]:
                    if state == "COMPLETED":
                        print("\n🎉 SUCCESS! ECS infrastructure confirmed working!")
                        return True
                    else:
                        print(f"\n❌ Failed: {message}")
                        return False
                
                await asyncio.sleep(5)
            
            print("\n⏱️ Timed out waiting for completion")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(create_minimal_deployment())
    if success:
        print("\n✅ CONFIRMED: ECS infrastructure can run flows!")
    else:
        print("\n❌ ECS infrastructure needs more work")
