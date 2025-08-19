#!/usr/bin/env python3
"""
Simple deployment script for Prefect Cloud
"""
import asyncio
from prefect.deployments import Deployment
from my_prefect_flow import my_first_flow

async def create_deployment():
    """Create a deployment for the flow"""
    
    print("🚀 Creating deployment...")
    
    deployment = await Deployment.build_from_flow(
        flow=my_first_flow,
        name="my-first-flow-ecs",
        work_pool_name="gellc-ecs-pool",
        description="GELLC Prefect flow running on ECS",
        version="1.0.0",
        tags=["ecs", "gellc", "production"]
    )
    
    # Apply the deployment
    deployment_id = await deployment.apply()
    
    print(f"✅ Deployment created!")
    print(f"🔗 Deployment ID: {deployment_id}")
    print(f"📋 Name: my-first-flow-ecs")
    print(f"🏊 Work Pool: gellc-ecs-pool")
    
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_deployment())
    print(f"\n🎉 Success! Your flow is now deployed to Prefect Cloud!")
    print(f"\n📱 View in Prefect Cloud:")
    print(f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments")
    print(f"\n🔧 Next steps:")
    print(f"1. Your ECS containers will automatically start as workers when flows are triggered")
    print(f"2. Go to Prefect Cloud and trigger a flow run")
    print(f"3. Watch it execute on your ECS infrastructure!")
