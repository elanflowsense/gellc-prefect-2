#!/usr/bin/env python3
"""
Trigger a test flow run to verify S3 + ECS integration
"""
import asyncio
from prefect.client.orchestration import get_client

async def trigger_test_run():
    """Trigger a new flow run for testing"""
    
    print("🧪 Triggering S3 + ECS Test Run")
    print("=" * 40)
    
    async with get_client() as client:
        try:
            # Get S3 deployment
            deployments = await client.read_deployments()
            
            s3_deployment = None
            for deployment in deployments:
                if deployment.name == "s3-ecs-flow":
                    s3_deployment = deployment
                    break
            
            if not s3_deployment:
                print("❌ Could not find 's3-ecs-flow' deployment")
                return None
            
            print(f"✅ Found deployment: {s3_deployment.name}")
            print(f"   Work Pool: {s3_deployment.work_pool_name}")
            
            # Check work pools first
            print(f"\n🔍 Checking work pools...")
            work_pools = await client.read_work_pools()
            for pool in work_pools:
                print(f"   - {pool.name} (type: {pool.type}, paused: {pool.is_paused})")
            
            # Trigger flow run
            print(f"\n🚀 Triggering new flow run...")
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=s3_deployment.id,
                parameters={"name": "Final Test - S3 + ECS"}
            )
            
            print(f"✅ Flow run created: {flow_run.id}")
            print(f"   State: {flow_run.state.type}")
            print(f"   Name: {flow_run.name}")
            print(f"   URL: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
            
            print(f"\n💡 Monitor this flow run in:")
            print(f"   1. Prefect Cloud UI (link above)")
            print(f"   2. ECS CloudWatch logs")
            print(f"   3. Wait ~1-2 minutes for worker to pick it up")
            
            return flow_run.id
            
        except Exception as e:
            print(f"❌ Error triggering flow run: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    flow_run_id = asyncio.run(trigger_test_run())
    
    if flow_run_id:
        print(f"\n🎯 Test flow run triggered successfully!")
        print(f"   Flow Run ID: {flow_run_id}")
        print(f"\n🔍 To debug if it fails:")
        print(f"   1. Check ECS task logs in CloudWatch")
        print(f"   2. Verify worker is connected to 'gellc-process-pool'")
        print(f"   3. Check Prefect Cloud UI for detailed logs")
    else:
        print(f"\n❌ Failed to trigger test flow run")
