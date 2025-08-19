#!/usr/bin/env python3
"""
Update the deployment to use gellc-process-pool instead of gellc-ecs-final
"""
import asyncio
from prefect import get_client

async def update_deployment_workpool():
    """Update deployment to use the running process pool"""
    
    deployment_id = "bfa29b27-5f1d-49ef-912a-543295b61751"
    
    print("🔧 Updating deployment to use gellc-process-pool...")
    print("=" * 50)
    
    async with get_client() as client:
        
        # Get current deployment
        deployment = await client.read_deployment(deployment_id)
        print(f"📦 Current deployment: {deployment.name}")
        print(f"🏊 Current work pool: {deployment.work_pool_name}")
        
        # Check that gellc-process-pool exists and has workers
        print(f"\n🔍 Checking gellc-process-pool status...")
        try:
            process_pool = await client.read_work_pool("gellc-process-pool")
            print(f"✅ Work pool exists: {process_pool.name} (Type: {process_pool.type})")
            
            # Check for workers
            workers = await client.read_workers_for_work_pool("gellc-process-pool")
            print(f"✅ Active workers: {len(workers)}")
            for worker in workers:
                print(f"  - {worker.name} (Last seen: {worker.last_heartbeat_time})")
                
        except Exception as e:
            print(f"❌ Error checking process pool: {e}")
            return
        
        # Update the deployment work pool
        print(f"\n🔄 Updating deployment work pool...")
        try:
            await client.update_deployment(
                deployment_id,
                work_pool_name="gellc-process-pool",
                work_queue_name="default"
            )
            print(f"✅ Deployment updated successfully!")
            
            # Verify the update
            updated_deployment = await client.read_deployment(deployment_id)
            print(f"📦 Updated work pool: {updated_deployment.work_pool_name}")
            
            print(f"\n🎉 Your deployment should now show as 'Ready' instead of 'Late'!")
            print(f"🔗 Check it here: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments/deployment/{deployment_id}")
            
            # Create a test flow run
            print(f"\n🎯 Creating test flow run...")
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=deployment_id,
                parameters={"name": "Process Pool Test"}
            )
            
            print(f"✅ Test flow run created: {flow_run.id}")
            print(f"📋 Flow run name: {flow_run.name}")
            print(f"🔗 Flow run URL: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
            
        except Exception as e:
            print(f"❌ Error updating deployment: {e}")

if __name__ == "__main__":
    asyncio.run(update_deployment_workpool())
