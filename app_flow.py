#!/usr/bin/env python3
"""
Simple flow file that will be available in the container's /app directory
"""
from prefect import flow, task

@task
def app_task(name: str = "App"):
    """Task that works from /app directory"""
    message = f"🎉 SUCCESS! {name} from /app directory in ECS!"
    print(message)
    print("✅ Running from /app directory in ECS container!")
    print("📁 Using container's working directory!")
    print("🐳 ECS + Process Workers + /app = SUCCESS!")
    return message

@flow
def app_flow(name: str = "App"):
    """Flow that works from /app directory"""
    print(f"🚀 Starting /APP flow for: {name}")
    print("📁 Working from /app directory in container")
    print("🐳 ECS container execution") 
    print("☁️ Orchestrated by Prefect Cloud")
    
    result = app_task(name)
    
    print(f"📊 Flow result: {result}")
    print("🏁 /APP flow completed successfully!")
    return result

if __name__ == "__main__":
    # This allows the flow to be run directly for testing
    app_flow(name="Local Test")
