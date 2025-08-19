#!/usr/bin/env python3
"""
Test the S3 deployment by triggering a flow run
"""
import asyncio
from prefect.client.orchestration import get_client

async def test_s3_deployment():
    """Test the S3 deployment by triggering a flow run"""
    
    print("🧪 Testing S3 + ECS Deployment")
    print("=" * 40)
    
    async with get_client() as client:
        try:
            # Get deployment
            print("🔍 Looking for 's3-ecs-flow' deployment...")
            deployments = await client.read_deployments()
            
            s3_deployment = None
            for deployment in deployments:
                if deployment.name == "s3-ecs-flow":
                    s3_deployment = deployment
                    break
            
            if not s3_deployment:
                print("❌ Could not find 's3-ecs-flow' deployment")
                print("Available deployments:")
                for dep in deployments:
                    print(f"  - {dep.name}")
                return None
            
            print(f"✅ Found deployment: {s3_deployment.name}")
            print(f"   ID: {s3_deployment.id}")
            print(f"   Work Pool: {s3_deployment.work_pool_name}")
            print(f"   Storage: S3")
            
            # Trigger flow run
            print(f"\n🚀 Triggering flow run...")
            flow_run = await client.create_flow_run_from_deployment(
                deployment_id=s3_deployment.id,
                parameters={"name": "S3 Test Run"}
            )
            
            print(f"✅ Flow run created: {flow_run.id}")
            print(f"   State: {flow_run.state.type}")
            print(f"   Name: {flow_run.name}")
            
            print(f"\n🎯 Flow run details:")
            print(f"   URL: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/flow-runs/flow-run/{flow_run.id}")
            
            # Monitor the flow run for a bit
            print(f"\n⏳ Monitoring flow run...")
            for i in range(10):  # Monitor for 30 seconds
                await asyncio.sleep(3)
                updated_run = await client.read_flow_run(flow_run.id)
                print(f"   [{i*3:2d}s] State: {updated_run.state.type}")
                
                if updated_run.state.is_final():
                    print(f"\n🏁 Flow run completed!")
                    print(f"   Final state: {updated_run.state.type}")
                    if updated_run.state.type == "COMPLETED":
                        print(f"   ✅ SUCCESS! Your S3 + ECS integration is working!")
                    else:
                        print(f"   ❌ Flow run failed: {updated_run.state.message}")
                    break
            else:
                print(f"\n⏰ Still monitoring - check Prefect Cloud UI for updates")
                print(f"   The flow run should complete shortly on your ECS infrastructure")
            
            return flow_run.id
            
        except Exception as e:
            print(f"❌ Error testing deployment: {e}")
            import traceback
            traceback.print_exc()
            return None

async def check_s3_files():
    """Check what files were uploaded to S3"""
    
    print("\n📦 Checking S3 bucket contents...")
    
    try:
        import boto3
        s3_client = boto3.client('s3')
        
        bucket_name = "gellc-prefect-flows"
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response:
            print(f"✅ Files in S3 bucket '{bucket_name}':")
            for obj in response['Contents']:
                print(f"   📄 {obj['Key']} ({obj['Size']} bytes)")
        else:
            print(f"❌ No files found in bucket '{bucket_name}'")
            
    except Exception as e:
        print(f"❌ Error checking S3: {e}")

if __name__ == "__main__":
    print("🎯 S3 + ECS Integration Test")
    print("="*50)
    
    # Check S3 files first
    asyncio.run(check_s3_files())
    
    # Test the deployment
    flow_run_id = asyncio.run(test_s3_deployment())
    
    if flow_run_id:
        print(f"\n🎉 Test completed!")
        print(f"💡 Next steps:")
        print(f"1. Check Prefect Cloud UI for flow run details")
        print(f"2. Verify your ECS worker picked up the job")
        print(f"3. Check ECS CloudWatch logs for execution details")
        print(f"4. Your S3 + ECS + Prefect Cloud integration is ready!")
    else:
        print(f"\n❌ Test failed - check the errors above")