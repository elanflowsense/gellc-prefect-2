#!/usr/bin/env python3
"""
Trigger a flow run via API and monitor it
"""
import asyncio
import time
from prefect import get_client

async def trigger_and_monitor_flow_run():
    """Trigger a flow run and monitor its progress"""
    
    print("🚀 Triggering flow run via API...")
    
    try:
        async with get_client() as client:
            # Get the deployment
            deployments = await client.read_deployments()
            target_deployment = None
            
            for deployment in deployments:
                if deployment.name == "my-first-flow-ecs":
                    target_deployment = deployment
                    break
            
            if not target_deployment:
                print("❌ Deployment 'my-first-flow-ecs' not found")
                return
            
            print(f"✅ Found deployment: {target_deployment.name}")
            print(f"🔗 Deployment ID: {target_deployment.id}")
            print(f"🏊 Work Pool: {target_deployment.work_pool_name}")
            
            # Create a flow run
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=target_deployment.id,
                state=None  # Let it start immediately
            )
            
            print(f"\n🎯 Created flow run: {flow_run.id}")
            print(f"📋 Flow run name: {flow_run.name}")
            print(f"⏰ Created at: {flow_run.created}")
            print(f"🔄 Initial state: {flow_run.state.type}")
            
            # Monitor the flow run for a few minutes
            print(f"\n👀 Monitoring flow run progress...")
            
            for i in range(24):  # Monitor for 2 minutes (24 * 5 seconds)
                # Get updated flow run info
                updated_flow_run = await client.read_flow_run(flow_run.id)
                
                print(f"[{i*5:3d}s] State: {updated_flow_run.state.type} | Message: {updated_flow_run.state.message or 'No message'}")
                
                # If completed or failed, get logs
                if updated_flow_run.state.type in ["COMPLETED", "FAILED", "CRASHED"]:
                    print(f"\n📊 Final state: {updated_flow_run.state.type}")
                    
                    # Try to get logs
                    try:
                        logs = await client.read_logs(flow_run_id=flow_run.id)
                        if logs:
                            print(f"\n📝 Flow run logs:")
                            for log in logs[-10:]:  # Last 10 log entries
                                print(f"  {log.timestamp}: {log.message}")
                        else:
                            print("📝 No logs available")
                    except Exception as e:
                        print(f"⚠️  Could not fetch logs: {e}")
                    
                    break
                
                await asyncio.sleep(5)
            else:
                print(f"\n⏱️  Flow run still in progress after 2 minutes")
            
            return flow_run
            
    except Exception as e:
        print(f"❌ Error triggering flow run: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    flow_run = asyncio.run(trigger_and_monitor_flow_run())
    if flow_run:
        print(f"\n🔗 View in Prefect Cloud:")
        print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
    else:
        print("❌ Failed to create flow run")
