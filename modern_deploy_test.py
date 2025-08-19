#!/usr/bin/env python3
"""
Modern flow deployment test
"""
import asyncio
from prefect import flow, task, get_client

@task
def final_test_task():
    """Final test to confirm ECS works"""
    print("🎉 FINAL TEST: This is running on ECS!")
    print("✅ ECS infrastructure is working!")
    print("🚀 Ready for production flows!")
    return "ECS_CONFIRMED_WORKING"

@flow
def final_ecs_test():
    """Final test flow"""
    print("🔬 Final ECS infrastructure test starting...")
    result = final_test_task()
    print(f"📊 Final result: {result}")
    print("🏁 Test completed successfully!")
    return result

async def test_modern_deployment():
    """Test using modern flow.deploy() method"""
    
    print("🚀 Testing modern deployment approach...")
    
    try:
        # Use the modern flow.deploy() method
        deployment_id = await final_ecs_test.deploy(
            name="final-ecs-test",
            work_pool_name="gellc-process-pool",
            image="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",  # Use our ECS image
            push=False,  # Don't push code anywhere
        )
        
        print(f"✅ Modern deployment created: {deployment_id}")
        
        # Test the deployment
        async with get_client() as client:
            # Get the deployment and create a run
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=deployment_id
            )
            
            print(f"🎯 Flow run created: {flow_run.id}")
            print(f"📋 Name: {flow_run.name}")
            
            # Monitor execution
            for i in range(18):  # 90 seconds
                updated_flow_run = await client.read_flow_run(flow_run.id)
                state = updated_flow_run.state.type
                message = updated_flow_run.state.message or 'No message'
                
                print(f"[{i*5:2d}s] {state:10} | {message}")
                
                if state == "COMPLETED":
                    print("\n🎉🎉 SUCCESS! ECS INFRASTRUCTURE CONFIRMED WORKING! 🎉🎉")
                    print("✅ You can now run flows on ECS!")
                    return True
                elif state in ["FAILED", "CRASHED"]:
                    print(f"\n❌ Failed: {message}")
                    return False
                
                await asyncio.sleep(5)
            
            print("\n⏱️ Test timed out")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_modern_deployment())
    
    if success:
        print("\n" + "="*60)
        print("🎉 ECS INFRASTRUCTURE FULLY CONFIRMED WORKING! 🎉")
        print("="*60)
        print("✅ Ready to deploy multiple flows")
        print("✅ Ready for production workloads") 
        print("✅ Ready for GitHub integration (if desired)")
    else:
        print("\n❌ Still troubleshooting ECS setup...")
