#!/usr/bin/env python3
"""
Create a fresh flow run to test if the workers are now working properly
"""
import asyncio
from prefect import get_client

async def create_fresh_flow_run():
    """Create a new flow run to test current worker capacity"""
    
    deployment_id = "8fb1cac6-0493-4da7-aacf-6383690fa2b1"  # VICTORY-s3-ecs-deployment
    
    print("🎯 Creating FRESH flow run to test workers...")
    print("=" * 50)
    
    async with get_client() as client:
        
        # Create new flow run
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "FRESH WORKER TEST"}
        )
        
        print(f"✅ NEW Flow Run Created:")
        print(f"  Flow Run ID: {flow_run.id}")
        print(f"  Flow Run Name: {flow_run.name}")
        print(f"  State: {flow_run.state.name}")
        print(f"  Work Pool: {flow_run.work_pool_name}")
        print(f"  Work Queue: {flow_run.work_queue_name}")
        
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"\n🔗 NEW Flow Run URL:")
        print(f"{base_url}/flow-runs/flow-run/{flow_run.id}")
        
        print(f"\n📋 This new flow run should start immediately!")
        print(f"🔄 Check if it transitions: Scheduled → Running → Completed")
        print(f"⏰ If this one also stays 'Late', there's a deeper worker issue")
        
        # Also check current worker queue status
        print(f"\n🔍 CHECKING WORK QUEUE STATUS:")
        try:
            work_queues = await client.read_work_queues(
                work_pool_name="gellc-process-pool",
                limit=5
            )
            
            for wq in work_queues:
                if wq.name == "default":
                    print(f"  Queue: {wq.name}")
                    print(f"  Is paused: {wq.is_paused}")
                    print(f"  Concurrency limit: {wq.concurrency_limit}")
                    print(f"  Priority: {wq.priority}")
                    break
            else:
                print("  ❌ 'default' work queue not found!")
                
        except Exception as e:
            print(f"  ❌ Error checking work queue: {e}")

if __name__ == "__main__":
    asyncio.run(create_fresh_flow_run())
