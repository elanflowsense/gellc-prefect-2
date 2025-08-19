#!/usr/bin/env python3
"""
Check the status of the REAL deployment and why it shows as "Late"
"""
import asyncio
from prefect import get_client

async def check_deployment_status():
    """Check deployment and work pool status"""
    
    deployment_id = "bfa29b27-5f1d-49ef-912a-543295b61751"
    
    print("🔍 Checking deployment status...")
    print("=" * 50)
    
    async with get_client() as client:
        
        # Get deployment details
        deployment = await client.read_deployment(deployment_id)
        print(f"📦 Deployment: {deployment.name}")
        print(f"🏊 Work Pool: {deployment.work_pool_name}")
        print(f"⏸️ Paused: {deployment.paused}")
        print(f"📅 Schedule Active: {deployment.is_schedule_active}")
        
        # Check work pool status
        print(f"\n🏊 Work Pool Status:")
        try:
            work_pool = await client.read_work_pool(deployment.work_pool_name)
            print(f"  Name: {work_pool.name}")
            print(f"  Type: {work_pool.type}")
            print(f"  Paused: {work_pool.is_paused}")
            print(f"  Default Queue: {work_pool.default_queue_id}")
            
            # Check for workers
            workers = await client.read_workers_for_work_pool(work_pool.name)
            print(f"  Active Workers: {len(workers)}")
            
            if not workers:
                print("  ❌ NO ACTIVE WORKERS - This is why it shows as 'Late'!")
                print("  💡 You need to start ECS workers to execute flows")
            else:
                for worker in workers:
                    print(f"    - {worker.name} (Last seen: {worker.last_heartbeat_time})")
        
        except Exception as e:
            print(f"  ❌ Error reading work pool: {e}")
        
        # Check recent flow runs
        print(f"\n🏃 Recent Flow Runs:")
        flow_runs = await client.read_flow_runs(
            deployment_filter={"id": {"any_": [deployment_id]}},
            limit=5
        )
        
        if not flow_runs:
            print("  No flow runs found")
        else:
            for run in flow_runs:
                print(f"  - {run.name}: {run.state.type} ({run.created})")
        
        # Check if there are pending/scheduled runs
        pending_runs = await client.read_flow_runs(
            state_filter={"type": {"any_": ["SCHEDULED", "PENDING"]}},
            deployment_filter={"id": {"any_": [deployment_id]}},
            limit=10
        )
        
        if pending_runs:
            print(f"\n⏰ Pending/Scheduled Runs: {len(pending_runs)}")
            for run in pending_runs:
                print(f"  - {run.name}: {run.state.type} (Expected: {run.expected_start_time})")
            print("  💡 These are waiting for workers - that's why it shows 'Late'")
        
        print(f"\n🛠️ How to fix 'Late' status:")
        print(f"1. Start ECS workers in your cluster")
        print(f"2. Or start a local worker for testing:")
        print(f"   prefect worker start --pool {deployment.work_pool_name}")
        print(f"3. Check if your ECS cluster has capacity")
        print(f"4. Verify ECS task definition has correct Prefect configuration")

if __name__ == "__main__":
    asyncio.run(check_deployment_status())
