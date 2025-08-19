#!/usr/bin/env python3
"""
Check the specific flow run that's showing as LATE
"""
import asyncio
from prefect import get_client

async def check_flow_run_status():
    """Check the specific flow run details"""
    
    flow_run_id = "068a3da3-1d57-7a2e-8000-9769b3a3fe5e"
    
    print(f"🔍 CHECKING FLOW RUN: {flow_run_id}")
    print("=" * 60)
    
    async with get_client() as client:
        
        try:
            # Get flow run details
            flow_run = await client.read_flow_run(flow_run_id)
            
            print(f"📋 FLOW RUN DETAILS:")
            print(f"  Name: {flow_run.name}")
            print(f"  State: {flow_run.state.name}")
            print(f"  Deployment ID: {flow_run.deployment_id}")
            print(f"  Work Pool: {flow_run.work_pool_name}")
            print(f"  Work Queue: {flow_run.work_queue_name}")
            print(f"  Created: {flow_run.created}")
            print(f"  Expected start time: {flow_run.expected_start_time}")
            print(f"  Start time: {flow_run.start_time}")
            
            if flow_run.deployment_id:
                print(f"\n📦 DEPLOYMENT DETAILS:")
                deployment = await client.read_deployment(flow_run.deployment_id)
                print(f"  Deployment Name: {deployment.name}")
                print(f"  Work Pool: {deployment.work_pool_name}")
                print(f"  Work Queue: {deployment.work_queue_name}")
                print(f"  Is paused: {deployment.is_paused}")
                print(f"  Schedule active: {deployment.schedule_active}")
            
            # Check if work queue has any issues
            if flow_run.work_pool_name and flow_run.work_queue_name:
                print(f"\n🔍 WORK QUEUE STATUS:")
                try:
                    work_queues = await client.read_work_queues(
                        work_pool_name=flow_run.work_pool_name,
                        limit=10
                    )
                    
                    target_queue = None
                    for wq in work_queues:
                        if wq.name == flow_run.work_queue_name:
                            target_queue = wq
                            break
                    
                    if target_queue:
                        print(f"  Queue Name: {target_queue.name}")
                        print(f"  Is paused: {target_queue.is_paused}")
                        print(f"  Concurrency limit: {target_queue.concurrency_limit}")
                        print(f"  Priority: {target_queue.priority}")
                    else:
                        print(f"  ❌ Work queue '{flow_run.work_queue_name}' not found!")
                        
                except Exception as e:
                    print(f"  ❌ Error checking work queue: {e}")
            
            # Suggest solutions
            print(f"\n💡 POTENTIAL SOLUTIONS:")
            if flow_run.state.name == "Late":
                print("  1. Check if the single active worker is busy with other tasks")
                print("  2. Restart the ECS service to potentially get more workers")
                print("  3. Scale up the ECS service to desired count = 2")
                print("  4. Check worker logs for any errors")
                
            elif flow_run.state.name == "Scheduled":
                print("  1. Flow is scheduled but not yet started - this is normal")
                print("  2. Check expected start time vs current time")
            
        except Exception as e:
            print(f"❌ Error reading flow run: {e}")

if __name__ == "__main__":
    asyncio.run(check_flow_run_status())
