#!/usr/bin/env python3
"""
Create a Process work pool that works with our ECS worker
"""
import asyncio
from prefect import get_client
from prefect.client.schemas.actions import WorkPoolCreate

async def create_process_work_pool():
    """Create a Process work pool for our ECS-hosted worker"""
    
    print("🗑️  Deleting ECS work pool...")
    
    try:
        async with get_client() as client:
            # Delete the existing ECS work pool
            await client.delete_work_pool("gellc-ecs-pool")
            print("✅ Deleted ECS work pool")
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Create new process work pool
            print("🏊 Creating Process work pool...")
            
            work_pool_data = WorkPoolCreate(
                name="gellc-process-pool",
                type="process",
                description="Process work pool for GELLC Prefect flows running on ECS",
                base_job_template={
                    "job_configuration": {
                        "command": "python {file_path}",
                        "env": {},
                        "working_dir": "/app",
                        "stream_output": True
                    },
                    "variables": {
                        "properties": {
                            "command": {
                                "title": "Command",
                                "description": "Command to run the flow",
                                "type": "string",
                                "default": "python {file_path}"
                            }
                        },
                        "type": "object"
                    }
                }
            )
            
            work_pool = await client.create_work_pool(work_pool=work_pool_data)
            
            print(f"✅ Successfully created Process work pool: {work_pool.name}")
            print(f"🔗 Work pool ID: {work_pool.id}")
            
            return work_pool
            
    except Exception as e:
        print(f"❌ Error creating work pool: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    work_pool = asyncio.run(create_process_work_pool())
    if work_pool:
        print("\n🎉 Process work pool created successfully!")
        print("🔄 Now we need to update the deployment to use this work pool")
    else:
        print("❌ Failed to create work pool")
