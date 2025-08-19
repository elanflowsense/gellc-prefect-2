#!/usr/bin/env python3
"""
Create a new deployment with the process work pool
"""
import asyncio
from prefect.deployments import Deployment
from my_prefect_flow import my_first_flow

async def create_new_deployment():
    """Create a new deployment with the correct work pool"""
    
    print("🚀 Creating new deployment with process work pool...")
    
    deployment = await Deployment.build_from_flow(
        flow=my_first_flow,
        name="my-first-flow-process",
        work_pool_name="gellc-process-pool",
        description="GELLC Prefect flow running on ECS with Process work pool",
        version="2.0.0",
        tags=["ecs", "gellc", "process", "production"]
    )
    
    # Apply the deployment
    deployment_id = await deployment.apply()
    
    print(f"✅ Deployment created!")
    print(f"🔗 Deployment ID: {deployment_id}")
    print(f"📋 Name: my-first-flow-process")
    print(f"🏊 Work Pool: gellc-process-pool")
    
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_new_deployment())
    print(f"\n🎉 Success! New deployment created!")
    print(f"\n📱 View in Prefect Cloud:")
    print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments")
    print(f"\n🚀 This deployment should now work with your ECS worker!")
