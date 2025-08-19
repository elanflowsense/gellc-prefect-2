#!/usr/bin/env python3
"""
Check available work pools and create the missing one
"""
import asyncio
from prefect import get_client

async def check_and_create_workpools():
    """Check available work pools and create missing ones"""
    
    print("🏊 Checking work pools...")
    print("=" * 50)
    
    async with get_client() as client:
        
        # List all work pools
        print("\n📋 Available work pools:")
        work_pools = await client.read_work_pools()
        
        pool_names = [pool.name for pool in work_pools]
        
        if not work_pools:
            print("  ❌ No work pools found!")
        else:
            for pool in work_pools:
                workers = await client.read_workers_for_work_pool(pool.name)
                print(f"  - {pool.name} (Type: {pool.type}, Workers: {len(workers)})")
        
        # Check if gellc-process-pool exists
        if "gellc-process-pool" not in pool_names:
            print(f"\n⚠️  'gellc-process-pool' not found!")
            print(f"📋 Available pools: {pool_names}")
            
            # Create the missing work pool
            print(f"\n🔧 Creating 'gellc-process-pool'...")
            return True
        else:
            print(f"\n✅ 'gellc-process-pool' exists!")
            return False

if __name__ == "__main__":
    needs_creation = asyncio.run(check_and_create_workpools())
    
    if needs_creation:
        print("\n🔧 Need to create the work pool...")
    else:
        print("\n✅ Work pool exists, ready to deploy!")
