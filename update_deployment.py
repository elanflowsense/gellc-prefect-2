#!/usr/bin/env python3
"""
Update deployment to use the new process work pool
"""
import asyncio
from prefect import get_client

async def update_deployment_work_pool():
    """Update the deployment to use the new process work pool"""
    
    print("🔄 Updating deployment work pool...")
    
    try:
        async with get_client() as client:
            # Get the current deployment
            deployments = await client.read_deployments()
            target_deployment = None
            
            for deployment in deployments:
                if deployment.name == "my-first-flow-ecs":
                    target_deployment = deployment
                    break
            
            if not target_deployment:
                print("❌ Deployment not found")
                return False
            
            print(f"📋 Found deployment: {target_deployment.name}")
            print(f"🏊 Current work pool: {target_deployment.work_pool_name}")
            
            # Update the deployment
            await client.update_deployment(
                deployment_id=target_deployment.id,
                work_pool_name="gellc-process-pool"
            )
            
            print(f"✅ Updated deployment work pool to: gellc-process-pool")
            
            return True
            
    except Exception as e:
        print(f"❌ Error updating deployment: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(update_deployment_work_pool())
    if success:
        print("\n🎉 Deployment updated successfully!")
    else:
        print("❌ Failed to update deployment")
