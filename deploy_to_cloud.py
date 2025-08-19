#!/usr/bin/env python3
"""
Deploy flow to Prefect Cloud
"""
import asyncio
from prefect import get_client
from prefect.deployments import Deployment
from my_prefect_flow import my_first_flow

async def deploy_flow_to_cloud():
    """Deploy the flow to Prefect Cloud"""
    
    print("🚀 Deploying flow to Prefect Cloud...")
    
    try:
        # Create deployment
        deployment = Deployment.build_from_flow(
            flow=my_first_flow,
            name="gellc-ecs-deployment",
            work_pool_name="gellc-ecs-pool",
            description="GELLC Prefect flow running on ECS",
            version="1.0.0",
            tags=["ecs", "gellc", "production"],
        )
        
        # Deploy to Prefect Cloud
        deployment_id = await deployment.apply()
        
        print(f"✅ Successfully deployed flow!")
        print(f"🔗 Deployment ID: {deployment_id}")
        print(f"📋 Deployment name: gellc-ecs-deployment")
        print(f"🏊 Work pool: gellc-ecs-pool")
        
        return deployment_id
        
    except Exception as e:
        print(f"❌ Failed to deploy flow: {e}")
        return None

if __name__ == "__main__":
    deployment_id = asyncio.run(deploy_flow_to_cloud())
    if deployment_id:
        print("\n🎉 Flow deployed successfully!")
        print("\nNext steps:")
        print("1. Go to Prefect Cloud UI to see your deployment")
        print("2. Start ECS worker to handle flow runs")
        print("3. Trigger flow runs from Prefect Cloud")
        print("\nPrefect Cloud URL:")
        print("https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d")
    else:
        print("❌ Failed to deploy flow")
