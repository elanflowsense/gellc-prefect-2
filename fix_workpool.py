#!/usr/bin/env python3
"""
Fix the ECS work pool configuration
"""
import asyncio
from prefect import get_client

async def fix_ecs_work_pool():
    """Fix the ECS work pool configuration"""
    
    print("🔧 Fixing ECS work pool configuration...")
    
    try:
        async with get_client() as client:
            # Get the work pool
            work_pool = await client.read_work_pool("gellc-ecs-pool")
            print(f"📋 Current work pool: {work_pool.name}")
            
            # Print current configuration for debugging
            print(f"🔍 Current base job template:")
            import json
            print(json.dumps(work_pool.base_job_template, indent=2))
            
            # Update the base job template to fix the command issue
            updated_template = work_pool.base_job_template.copy()
            updated_template["job_configuration"]["command"] = "./start.sh"  # String instead of list
            
            # Update the work pool
            await client.update_work_pool(
                work_pool_name="gellc-ecs-pool",
                base_job_template=updated_template
            )
            
            print("✅ Work pool configuration updated!")
            print("🔧 Changed command from ['./start.sh'] to './start.sh'")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing work pool: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(fix_ecs_work_pool())
    if success:
        print("\n🎉 Work pool fixed! Try running your flow again.")
    else:
        print("❌ Failed to fix work pool")
