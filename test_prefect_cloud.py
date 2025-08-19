#!/usr/bin/env python3
"""
Test script to verify Prefect Cloud connection
"""
import os
import sys
import asyncio
from prefect import get_client

async def test_prefect_cloud_connection():
    """Test connection to Prefect Cloud"""
    
    # Check if environment variables are set
    api_url = os.getenv('PREFECT_API_URL')
    api_key = os.getenv('PREFECT_API_KEY')
    
    if not api_url:
        print("❌ PREFECT_API_URL environment variable not set")
        print("Please set it to your Prefect Cloud API URL")
        print("Example: export PREFECT_API_URL='https://api.prefect.cloud/api/accounts/xxx/workspaces/xxx'")
        return False
        
    if not api_key:
        print("❌ PREFECT_API_KEY environment variable not set")
        print("Please set it to your Prefect Cloud API key")
        print("Example: export PREFECT_API_KEY='pnu_xxx'")
        return False
    
    print(f"🔗 Testing connection to: {api_url}")
    
    try:
        # Test the connection
        async with get_client() as client:
            # Try to get workspace info - test with a simple API call
            work_pools = await client.read_work_pools()
            print(f"✅ Successfully connected to Prefect Cloud!")
            print(f"🏊 Available work pools: {len(work_pools)}")
            for pool in work_pools:
                print(f"   - {pool.name} ({pool.type})")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to Prefect Cloud: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_prefect_cloud_connection())
    sys.exit(0 if success else 1)
