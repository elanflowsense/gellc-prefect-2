#!/usr/bin/env python3
"""
Simple approach: Put flow code in Docker image, reference by file path
"""
import asyncio
from prefect.deployments import Deployment
from prefect import get_client
from app_flow import app_flow  # Import the actual flow

async def create_embedded_deployment():
    """Create deployment that references flow code in Docker image"""
    
    print("🚀 Creating deployment with embedded code...")
    
    # Create deployment using the imported flow
    deployment = await Deployment.build_from_flow(
        flow=app_flow,  # The actual flow object
        name="EMBEDDED-code-deployment", 
        work_pool_name="gellc-process-pool",  # Your existing workers
        work_queue_name="default",
        entrypoint="app_flow.py:app_flow",  # This tells ECS where to find it
        # No storage block needed - code is in the image
        tags=["embedded", "simple", "working"],
        description="Flow code embedded in Docker image",
        version="1.0.0"
    )
    
    deployment_id = await deployment.apply()
    
    print(f"✅ Deployment created: {deployment_id}")
    print(f"✅ Flow file: app_flow.py (in Docker image)")
    print(f"✅ Entry point: app_flow:app_flow")
    
    # Test it
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=deployment_id,
            parameters={"name": "EMBEDDED TEST"}
        )
        print(f"✅ Test flow run: {flow_run.id}")
    
    return deployment_id

if __name__ == "__main__":
    asyncio.run(create_embedded_deployment())
