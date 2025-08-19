#!/usr/bin/env python3
"""
Check workspace and deployment details more thoroughly
"""
import asyncio
from prefect import get_client
import os

async def deep_workspace_check():
    """Deep check of workspace and deployments"""
    
    print("🔍 DEEP WORKSPACE & DEPLOYMENT CHECK")
    print("=" * 60)
    
    # Show current environment
    print("🌍 ENVIRONMENT INFO:")
    print(f"PREFECT_API_URL: {os.getenv('PREFECT_API_URL', 'Not set')}")
    print(f"PREFECT_API_KEY: {os.getenv('PREFECT_API_KEY', 'Not set')[:10]}...")
    print()
    
    async with get_client() as client:
        
        # Get the actual API URL being used
        print(f"🔗 Client API URL: {client.api_url}")
        print()
        
        # List ALL deployments without filters
        print("📋 ALL DEPLOYMENTS (no filters):")
        try:
            all_deployments = await client.read_deployments(limit=100)
            print(f"Total deployments found: {len(all_deployments)}")
            
            if not all_deployments:
                print("❌ NO DEPLOYMENTS FOUND!")
                return
            
            for i, dep in enumerate(all_deployments, 1):
                print(f"\n{i}. 📦 {dep.name}")
                print(f"   🆔 ID: {dep.id}")
                print(f"   📅 Created: {dep.created}")
                print(f"   🏷️ Tags: {dep.tags}")
                print(f"   🏊 Work Pool: {dep.work_pool_name}")
                print(f"   ⏸️ Paused: {dep.paused}")
                print(f"   📅 Schedule Active: {dep.is_schedule_active}")
                
                # Show the flow name too
                try:
                    flow = await client.read_flow(dep.flow_id)
                    print(f"   🌊 Flow Name: {flow.name}")
                except:
                    print(f"   🌊 Flow Name: [Error reading flow]")
        
        except Exception as e:
            print(f"❌ Error reading deployments: {e}")
            return
        
        # Check work pools
        print(f"\n🏊 WORK POOLS:")
        try:
            work_pools = await client.read_work_pools()
            for pool in work_pools:
                print(f"   - {pool.name} (Type: {pool.type})")
        except Exception as e:
            print(f"❌ Error reading work pools: {e}")
        
        # Show exact URLs for each deployment
        print(f"\n🔗 EXACT URLS FOR EACH DEPLOYMENT:")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        
        for i, dep in enumerate(all_deployments, 1):
            url = f"{base_url}/deployments/deployment/{dep.id}"
            print(f"{i}. {dep.name}: {url}")
        
        print(f"\n📱 MAIN DEPLOYMENTS PAGE:")
        print(f"{base_url}/deployments")

if __name__ == "__main__":
    asyncio.run(deep_workspace_check())
