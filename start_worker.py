#!/usr/bin/env python3
"""
Start a Prefect worker for testing
"""
import asyncio
from prefect.worker import serve

async def start_worker():
    """Start a process worker for the ECS work pool"""
    
    print("🔧 Starting Prefect worker...")
    print("🏊 Work Pool: gellc-ecs-pool")
    print("⏰ This will make your deployment show as 'Ready'")
    print("Press Ctrl+C to stop the worker")
    
    await serve(
        "gellc-ecs-pool",
        work_pool_type="process",  # Use process type for local testing
        limit=1
    )

if __name__ == "__main__":
    try:
        asyncio.run(start_worker())
    except KeyboardInterrupt:
        print("\n👋 Worker stopped")
