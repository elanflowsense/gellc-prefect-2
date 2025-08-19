#!/usr/bin/env python3
"""
Find where the gellc-process-pool workers are actually running
"""
import asyncio
from prefect import get_client
from datetime import datetime

async def investigate_workers():
    """Investigate where the process workers are running"""
    
    print("🔍 INVESTIGATING WORKER LOCATIONS")
    print("=" * 50)
    
    async with get_client() as client:
        
        # Get detailed info about the work pool
        print("🏊 WORK POOL DETAILS:")
        try:
            work_pool = await client.read_work_pool("gellc-process-pool")
            print(f"  Name: {work_pool.name}")
            print(f"  Type: {work_pool.type}")
            print(f"  Is paused: {work_pool.is_paused}")
            print(f"  Concurrency limit: {work_pool.concurrency_limit}")
            print(f"  Created: {work_pool.created}")
            
            # Check the base job template for clues
            if hasattr(work_pool, 'base_job_template') and work_pool.base_job_template:
                print(f"  Base job template: {work_pool.base_job_template}")
            
        except Exception as e:
            print(f"❌ Error reading work pool: {e}")
        
        # Get worker details
        print(f"\n👷 WORKER DETAILS:")
        try:
            workers = await client.read_workers_for_work_pool("gellc-process-pool")
            print(f"Total workers: {len(workers)}")
            
            for i, worker in enumerate(workers):
                print(f"\n  Worker {i+1}:")
                print(f"    ID: {worker.id}")
                print(f"    Name: {worker.name}")
                print(f"    Status: {worker.status}")
                print(f"    Last heartbeat: {worker.last_heartbeat_time}")
                
                # Try to get more details from worker
                if hasattr(worker, 'metadata') and worker.metadata:
                    print(f"    Metadata: {worker.metadata}")
                
                # Check worker's base job template
                if hasattr(worker, 'base_job_template') and worker.base_job_template:
                    print(f"    Base job template: {worker.base_job_template}")
                    
        except Exception as e:
            print(f"❌ Error reading workers: {e}")
        
        # Check recent flow runs to see execution environment
        print(f"\n📋 RECENT FLOW RUNS FROM THIS POOL:")
        try:
            from prefect.client.schemas.filters import FlowRunFilter, FlowRunFilterWorkPoolName
            from prefect.client.schemas.sorting import FlowRunSort
            
            # Get recent flow runs from this work pool
            flow_runs = await client.read_flow_runs(
                flow_run_filter=FlowRunFilter(
                    work_pool_name=FlowRunFilterWorkPoolName(any_=["gellc-process-pool"])
                ),
                sort=FlowRunSort.START_TIME_DESC,
                limit=5
            )
            
            if flow_runs:
                for run in flow_runs:
                    print(f"  Flow run: {run.name} ({run.state.name})")
                    print(f"    Started: {run.start_time}")
                    print(f"    Work pool: {run.work_pool_name}")
                    if hasattr(run, 'infrastructure_pid') and run.infrastructure_pid:
                        print(f"    Infrastructure PID: {run.infrastructure_pid}")
            else:
                print("  No recent flow runs found")
                
        except Exception as e:
            print(f"❌ Error reading flow runs: {e}")
        
        print(f"\n🔍 NEXT STEPS:")
        print("1. Check if workers are running on ECS/EC2/local machines")
        print("2. Look at worker logs in AWS CloudWatch (if ECS)")
        print("3. Check if workers are containerized or running directly")
        print("4. Determine where to install prefect-aws dependencies")

if __name__ == "__main__":
    asyncio.run(investigate_workers())
