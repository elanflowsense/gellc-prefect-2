#!/usr/bin/env python3
"""
Troubleshoot UI visibility issues
"""
import asyncio
from prefect import get_client

async def troubleshoot_deployments():
    """Debug why deployments aren't showing in UI"""
    
    print("🔍 TROUBLESHOOTING DEPLOYMENT VISIBILITY")
    print("=" * 60)
    
    async with get_client() as client:
        
        # Check client connection
        print("🔗 Testing Prefect Cloud connection...")
        try:
            # Test connection by reading deployments
            test_deployments = await client.read_deployments(limit=1)
            print(f"✅ Connected successfully!")
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return
        
        # List ALL deployments with more details
        print("\n📋 ALL DEPLOYMENTS IN YOUR ACCOUNT:")
        deployments = await client.read_deployments()
        
        if not deployments:
            print("❌ NO DEPLOYMENTS FOUND AT ALL!")
            print("This suggests a connection or workspace issue.")
            return
        
        for i, dep in enumerate(deployments, 1):
            print(f"\n{i}. NAME: {dep.name}")
            print(f"   ID: {dep.id}")
            print(f"   CREATED: {dep.created}")
            print(f"   TAGS: {dep.tags}")
            print(f"   WORK POOL: {dep.work_pool_name}")
            print(f"   PAUSED: {dep.paused}")
            print(f"   SCHEDULE ACTIVE: {dep.is_schedule_active}")
            
            # Exact URL for this deployment
            url = f"https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments/deployment/{dep.id}"
            print(f"   DIRECT URL: {url}")
        
        # Check workspace
        print(f"\n🏢 WORKSPACE INFO:")
        print(f"Account ID: ab61b83d-af98-4940-ac58-024d88160a03")
        print(f"Workspace ID: e31cc9e9-de96-4558-acdc-1ded94493b8d")
        
        # Main deployments page
        main_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d/deployments"
        print(f"Main deployments page: {main_url}")
        
        print(f"\n🛠️ TROUBLESHOOTING TIPS:")
        print(f"1. Try the main deployments URL above")
        print(f"2. Clear your browser cache")
        print(f"3. Try a different browser or incognito mode")
        print(f"4. Check if you have any filters applied in the UI")
        print(f"5. Look in the 'All' or 'Recent' tabs in the deployments page")
        print(f"6. Try searching for deployment names in the search box")

if __name__ == "__main__":
    asyncio.run(troubleshoot_deployments())
