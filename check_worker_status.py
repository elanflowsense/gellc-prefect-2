#!/usr/bin/env python3
"""
Check the current status of workers and work pool
"""
import asyncio
from prefect import get_client

async def check_worker_status():
    """Check workers and work pool status"""
    
    print("🔍 CHECKING WORKER STATUS")
    print("=" * 40)
    
    async with get_client() as client:
        
        # Check work pool
        print("🏊 WORK POOL STATUS:")
        try:
            work_pool = await client.read_work_pool("gellc-process-pool")
            print(f"  Name: {work_pool.name}")
            print(f"  Type: {work_pool.type}")
            print(f"  Is paused: {work_pool.is_paused}")
            print(f"  Concurrency limit: {work_pool.concurrency_limit}")
        except Exception as e:
            print(f"❌ Error reading work pool: {e}")
        
        # Check workers
        print(f"\n👷 WORKERS:")
        try:
            workers = await client.read_workers_for_work_pool("gellc-process-pool")
            print(f"Total workers: {len(workers)}")
            
            if workers:
                for i, worker in enumerate(workers):
                    print(f"\n  Worker {i+1}:")
                    print(f"    Name: {worker.name}")
                    print(f"    Status: {worker.status}")
                    print(f"    Last heartbeat: {worker.last_heartbeat_time}")
                    
                    # Check how recent the heartbeat is
                    import datetime
                    if worker.last_heartbeat_time:
                        now = datetime.datetime.now(datetime.timezone.utc)
                        time_diff = now - worker.last_heartbeat_time
                        print(f"    Heartbeat age: {time_diff.total_seconds():.1f} seconds ago")
                        
                        if time_diff.total_seconds() > 60:
                            print(f"    ⚠️ WARNING: Heartbeat is {time_diff.total_seconds():.1f}s old (>60s)")
                        else:
                            print(f"    ✅ Heartbeat is recent")
            else:
                print("  ❌ No workers found!")
                
        except Exception as e:
            print(f"❌ Error reading workers: {e}")
        
        # Check recent flow runs
        print(f"\n📋 RECENT FLOW RUNS:")
        try:
            from prefect.client.schemas.filters import FlowRunFilter, FlowRunFilterWorkPoolName
            from prefect.client.schemas.sorting import FlowRunSort
            
            flow_runs = await client.read_flow_runs(
                limit=5,
                sort=FlowRunSort.START_TIME_DESC
            )
            
            if flow_runs:
                for run in flow_runs:
                    print(f"  - {run.name} ({run.state.name}) - Work pool: {run.work_pool_name}")
                    print(f"    Created: {run.created}")
                    if run.start_time:
                        print(f"    Started: {run.start_time}")
                    else:
                        print(f"    Started: Not yet started")
            else:
                print("  No recent flow runs found")
                
        except Exception as e:
            print(f"❌ Error reading flow runs: {e}")

if __name__ == "__main__":
    asyncio.run(check_worker_status())
