#!/usr/bin/env python3
"""
Activate the s3-ecs-flow-modern deployment
"""
import asyncio
from prefect import get_client

async def activate_deployment():
    """Activate the s3-ecs-flow-modern deployment"""
    
    deployment_id = "9d685a68-a900-4b62-b2d1-021658799f41"
    
    print(f"🔧 Activating deployment: s3-ecs-flow-modern")
    print(f"📋 Deployment ID: {deployment_id}")
    print()
    
    async with get_client() as client:
        
        # Get current deployment
        deployment = await client.read_deployment(deployment_id)
        print(f"Current status:")
        print(f"  Name: {deployment.name}")
        print(f"  Schedule Active: {deployment.is_schedule_active}")
        print(f"  Paused: {deployment.paused}")
        
        # Update deployment to be active
        try:
            await client.set_deployment_paused_state(deployment_id, paused=False)
            print(f"✅ Deployment unpaused successfully")
        except Exception as e:
            print(f"⚠️  Note: {e}")
        
        # Read updated deployment
        updated_deployment = await client.read_deployment(deployment_id)
        print(f"\nUpdated status:")
        print(f"  Schedule Active: {updated_deployment.is_schedule_active}")
        print(f"  Paused: {updated_deployment.paused}")
        
        # Try to create a manual flow run to test
        print(f"\n🎯 Creating test flow run...")
        try:
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=deployment_id,
                parameters={"name": "Manual Test"}
            )
            print(f"✅ Flow run created: {flow_run.id}")
            print(f"📋 Flow run name: {flow_run.name}")
            print(f"🔗 View in UI: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
            
        except Exception as e:
            print(f"❌ Error creating flow run: {e}")
            
        print(f"\n🔗 Deployment URL:")
        print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments/deployment/{deployment_id}")

if __name__ == "__main__":
    asyncio.run(activate_deployment())
