#!/usr/bin/env python3
"""
Final working ECS setup
"""
import asyncio
from prefect import flow, task, get_client
from prefect.client.schemas.actions import WorkPoolCreate

@task
def victory_task():
    """Victory task"""
    print("🎉 VICTORY! ECS is working!")
    print("✅ Flow executed successfully on ECS infrastructure!")
    return "SUCCESS"

@flow
def victory_flow():
    """Victory flow"""
    print("🚀 Victory flow starting on ECS...")
    result = victory_task()
    print(f"📊 Result: {result}")
    return result

async def setup_working_ecs():
    """Set up a properly working ECS configuration"""
    
    print("🔧 Setting up working ECS configuration...")
    
    async with get_client() as client:
        # Delete existing work pools
        try:
            await client.delete_work_pool("gellc-process-pool")
            print("Deleted process work pool")
        except:
            pass
        
        try: 
            await client.delete_work_pool("gellc-ecs-pool")
            print("Deleted old ECS work pool")
        except:
            pass
        
        await asyncio.sleep(2)
        
        # Create proper ECS work pool
        work_pool_data = WorkPoolCreate(
            name="gellc-ecs-final",
            type="ecs",
            description="Final working ECS work pool",
            base_job_template={
                "job_configuration": {
                    "family": "gellc-prefect-task",
                    "image": "576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest",
                    "cluster": "gellc-prefect-cluster",
                    "cpu": 256,
                    "memory": 512,
                    "taskRoleArn": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
                    "executionRoleArn": "arn:aws:iam::576671272815:role/ecsTaskExecutionRole",
                    "launchType": "FARGATE",
                    "networkConfiguration": {
                        "awsvpcConfiguration": {
                            "subnets": ["subnet-74ebae28", "subnet-30f38b57"],
                            "securityGroups": ["sg-07df2040c0081cac5"],
                            "assignPublicIp": "ENABLED"
                        }
                    },
                    "region": "us-east-1",
                    "env": {
                        "PYTHONPATH": "/app"
                    }
                },
                "variables": {
                    "type": "object",
                    "properties": {
                        "image": {
                            "title": "Image",
                            "type": "string",
                            "default": "576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest"
                        }
                    }
                }
            }
        )
        
        work_pool = await client.create_work_pool(work_pool=work_pool_data)
        print(f"✅ Created ECS work pool: {work_pool.name}")
        
        # Deploy the victory flow
        deployment_id = await victory_flow.deploy(
            name="victory-flow",
            work_pool_name="gellc-ecs-final",
            image="576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest"
        )
        
        print(f"✅ Deployed victory flow: {deployment_id}")
        
        # Test it
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id
        )
        
        print(f"🎯 Created flow run: {flow_run.id}")
        
        # Monitor
        for i in range(20):
            updated_flow_run = await client.read_flow_run(flow_run.id)
            state = updated_flow_run.state.type
            message = updated_flow_run.state.message or 'No message'
            
            print(f"[{i*5:2d}s] {state:10} | {message}")
            
            if state == "COMPLETED":
                print("\n🎉🎉🎉 CONFIRMED: ECS CAN RUN FLOWS! 🎉🎉🎉")
                return True
            elif state in ["FAILED", "CRASHED"]:
                print(f"\n❌ Still failed: {message}")
                return False
            
            await asyncio.sleep(5)
        
        return False

if __name__ == "__main__":
    success = asyncio.run(setup_working_ecs())
    if success:
        print("\n" + "="*70)
        print("🎉 CONFIRMED: ECS INFRASTRUCTURE IS WORKING AND CAN RUN FLOWS! 🎉")
        print("="*70)
    else:
        print("\n❌ Still needs work")
