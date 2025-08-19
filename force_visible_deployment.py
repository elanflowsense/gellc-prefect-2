#!/usr/bin/env python3
"""
Force create a visible deployment using serve() method
"""
import asyncio
from prefect import flow, task, serve

@task
def simple_ecs_task(name: str = "ECS"):
    """Simple task for ECS"""
    message = f"🎉 Hello {name} from ECS!"
    print(message)
    print("✅ This is running on ECS infrastructure!")
    return message

@flow(name="VISIBLE-ECS-FLOW")
def visible_ecs_flow(name: str = "ECS"):
    """Flow that should be visible in UI"""
    print(f"🚀 Starting VISIBLE flow for: {name}")
    result = simple_ecs_task(name)
    print(f"📊 Result: {result}")
    print("🏁 VISIBLE flow completed!")
    return result

if __name__ == "__main__":
    print("🚀 Creating VISIBLE deployment using serve()...")
    
    # Use serve() which creates a deployment and should be visible
    visible_ecs_flow.serve(
        name="VISIBLE-ECS-DEPLOYMENT",
        work_pool_name="gellc-ecs-pool",
        tags=["VISIBLE", "ECS", "WORKING"],
        description="This deployment SHOULD be visible in Prefect Cloud UI",
        version="1.0.0",
        parameters={"name": "VISIBLE ECS"},
        limit=1  # Only run one at a time
    )
