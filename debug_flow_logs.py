#!/usr/bin/env python3
"""
Debug the flow run to see what went wrong
"""
import asyncio
from prefect.client.orchestration import get_client

async def debug_latest_flow_run():
    """Debug the latest flow run to see what went wrong"""
    
    print("🔍 Debugging Latest Flow Run")
    print("=" * 40)
    
    async with get_client() as client:
        try:
            # Get latest flow runs
            flow_runs = await client.read_flow_runs(limit=5)
            
            if not flow_runs:
                print("❌ No flow runs found")
                return
            
            latest_run = flow_runs[0]
            print(f"🔍 Latest flow run: {latest_run.name}")
            print(f"   ID: {latest_run.id}")
            print(f"   State: {latest_run.state.type}")
            print(f"   Message: {latest_run.state.message}")
            
            if latest_run.state.type == "CRASHED":
                print(f"\n📋 Crash details:")
                if hasattr(latest_run.state, 'data') and latest_run.state.data:
                    print(f"   Data: {latest_run.state.data}")
                
            # Get flow run logs
            print(f"\n📃 Flow run logs:")
            logs = await client.read_logs(
                log_filter={"flow_run_id": {"any_": [latest_run.id]}}
            )
            
            if logs:
                for log in logs:
                    level = log.level
                    message = log.message
                    timestamp = log.timestamp
                    print(f"   [{timestamp}] {level}: {message}")
            else:
                print("   No logs found - this might indicate the worker didn't pick up the job")
            
            # Check if there are any workers available
            print(f"\n🤖 Checking work pool status...")
            work_pools = await client.read_work_pools()
            
            for pool in work_pools:
                if pool.name == "gellc-process-pool":
                    print(f"✅ Work pool '{pool.name}' found")
                    print(f"   Type: {pool.type}")
                    print(f"   Is paused: {pool.is_paused}")
                    break
            else:
                print("❌ Work pool 'gellc-process-pool' not found")
            
            # Check recent deployments
            print(f"\n📦 Recent deployments:")
            deployments = await client.read_deployments(limit=3)
            for dep in deployments:
                print(f"   - {dep.name} (Work Pool: {dep.work_pool_name})")
            
        except Exception as e:
            print(f"❌ Error debugging: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_latest_flow_run())
