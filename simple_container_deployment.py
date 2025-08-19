#!/usr/bin/env python3
"""
Create a simple deployment without storage
"""
import asyncio
from prefect.deployments import Deployment
from my_prefect_flow import my_first_flow

async def create_simple_deployment():
    """Create a simple deployment without storage"""
    
    print("🚀 Creating simple deployment...")
    
    deployment = await Deployment.build_from_flow(
        flow=my_first_flow,
        name="my-first-flow-simple",
        work_pool_name="gellc-process-pool",
        description="Simple GELLC Prefect flow for container",
        version="4.0.0",
        tags=["ecs", "gellc", "simple", "production"],
        # Don't specify storage - let it use the flow directly
    )
    
    # Apply the deployment
    deployment_id = await deployment.apply()
    
    print(f"✅ Simple deployment created!")
    print(f"🔗 Deployment ID: {deployment_id}")
    print(f"📋 Name: my-first-flow-simple")
    print(f"🏊 Work Pool: gellc-process-pool")
    
    return deployment_id

if __name__ == "__main__":
    deployment_id = asyncio.run(create_simple_deployment())
    print(f"\n🎉 Success! Simple deployment created!")
    print(f"\n🚀 This deployment should reference the flow directly!")
