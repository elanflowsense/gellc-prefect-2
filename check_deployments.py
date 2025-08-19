#!/usr/bin/env python3
"""
Check all deployments and their visibility status
"""
import asyncio
from prefect import get_client

async def check_all_deployments():
    """List all deployments with detailed information"""
    
    print("🔍 Checking all deployments...")
    print("=" * 60)
    
    async with get_client() as client:
        
        # Get all deployments
        deployments = await client.read_deployments()
        
        if not deployments:
            print("❌ No deployments found!")
            return
        
        print(f"📋 Found {len(deployments)} deployment(s):")
        print()
        
        for i, deployment in enumerate(deployments, 1):
            print(f"{i}. Deployment: {deployment.name}")
            print(f"   ID: {deployment.id}")
            print(f"   Work Pool: {deployment.work_pool_name}")
            print(f"   Status: {'🟢 Active' if not deployment.is_schedule_active else '🔴 Inactive'}")
            print(f"   Tags: {deployment.tags}")
            print(f"   Created: {deployment.created}")
            print(f"   Updated: {deployment.updated}")
            
            # Check if flow exists
            try:
                flow = await client.read_flow(deployment.flow_id)
                print(f"   Flow: ✅ {flow.name}")
            except Exception as e:
                print(f"   Flow: ❌ Error: {e}")
            
            # Check work pool
            try:
                work_pool = await client.read_work_pool(deployment.work_pool_name)
                print(f"   Work Pool Status: ✅ {work_pool.type} pool exists")
            except Exception as e:
                print(f"   Work Pool Status: ❌ Error: {e}")
            
            print(f"   URL: https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments/deployment/{deployment.id}")
            print()

if __name__ == "__main__":
    asyncio.run(check_all_deployments())
