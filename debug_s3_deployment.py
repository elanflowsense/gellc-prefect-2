#!/usr/bin/env python3
"""
Debug the s3-ecs-flow deployment and test it via Prefect API
"""
import asyncio
import json
from prefect import get_client

async def debug_s3_deployment():
    """Debug and test the s3-ecs-flow deployment"""
    
    print("🔍 Debugging s3-ecs-flow deployment...")
    print("=" * 50)
    
    async with get_client() as client:
        
        # 1. List all deployments to find s3-ecs-flow
        print("\n📋 Listing all deployments...")
        deployments = await client.read_deployments()
        
        s3_deployment = None
        for deployment in deployments:
            print(f"  - {deployment.name} (ID: {deployment.id})")
            if deployment.name == "s3-ecs-flow":
                s3_deployment = deployment
                print(f"    ✅ Found s3-ecs-flow deployment!")
        
        if not s3_deployment:
            print("❌ s3-ecs-flow deployment not found!")
            print("💡 Available deployments:")
            for deployment in deployments:
                print(f"  - {deployment.name}")
            return None
        
        # 2. Get deployment details
        print(f"\n📊 Deployment Details:")
        print(f"  Name: {s3_deployment.name}")
        print(f"  ID: {s3_deployment.id}")
        print(f"  Work Pool: {s3_deployment.work_pool_name}")
        print(f"  Work Queue: {s3_deployment.work_queue_name}")
        print(f"  Entrypoint: {s3_deployment.entrypoint}")
        print(f"  Storage: {s3_deployment.storage_document_id}")
        print(f"  Infrastructure: {s3_deployment.infrastructure_document_id}")
        print(f"  Version: {s3_deployment.version}")
        print(f"  Tags: {s3_deployment.tags}")
        
        # 3. Check work pool
        print(f"\n🏊 Work Pool Status:")
        try:
            work_pool = await client.read_work_pool(s3_deployment.work_pool_name)
            print(f"  ✅ Work pool '{work_pool.name}' exists")
            print(f"  Type: {work_pool.type}")
            print(f"  Status: {work_pool.is_paused}")
            
            # Check for workers
            workers = await client.read_workers_for_work_pool(work_pool.name)
            print(f"  Workers: {len(workers)} active")
            for worker in workers:
                print(f"    - {worker.name} (Last seen: {worker.last_heartbeat_time})")
                
        except Exception as e:
            print(f"  ❌ Work pool error: {e}")
        
        # 4. Check storage configuration
        print(f"\n📦 Storage Configuration:")
        if s3_deployment.storage_document_id:
            try:
                storage_doc = await client.read_block_document(s3_deployment.storage_document_id)
                print(f"  ✅ Storage document exists")
                print(f"  Type: {storage_doc.block_type.name}")
                print(f"  Data: {json.dumps(storage_doc.data, indent=2)}")
            except Exception as e:
                print(f"  ❌ Storage error: {e}")
        else:
            print("  ⚠️  No storage document configured")
        
        # 5. Try to create a flow run
        print(f"\n🎯 Testing Flow Run Creation...")
        try:
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=s3_deployment.id,
                parameters={"name": "Debug Test"}
            )
            
            print(f"  ✅ Flow run created: {flow_run.id}")
            print(f"  Name: {flow_run.name}")
            print(f"  State: {flow_run.state.type}")
            
            # 6. Monitor the flow run for 60 seconds
            print(f"\n⏱️  Monitoring flow run for 60 seconds...")
            for i in range(12):
                updated_flow_run = await client.read_flow_run(flow_run.id)
                state = updated_flow_run.state
                
                print(f"  [{i*5:2d}s] State: {state.type:12} | Message: {state.message or 'No message'}")
                
                if state.type in ["COMPLETED", "FAILED", "CRASHED"]:
                    print(f"\n📊 Final State: {state.type}")
                    if state.type != "COMPLETED":
                        print(f"❌ Error: {state.message}")
                        
                        # Get flow run logs
                        print(f"\n📋 Flow Run Logs:")
                        try:
                            logs = await client.read_logs(
                                log_filter={"flow_run_id": {"any_": [flow_run.id]}}
                            )
                            for log in logs:
                                print(f"  {log.timestamp} [{log.level}] {log.message}")
                        except Exception as e:
                            print(f"  ❌ Error reading logs: {e}")
                    else:
                        print(f"🎉 SUCCESS! Flow completed successfully!")
                    
                    break
                
                await asyncio.sleep(5)
            
            return flow_run
            
        except Exception as e:
            print(f"  ❌ Error creating flow run: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    asyncio.run(debug_s3_deployment())
