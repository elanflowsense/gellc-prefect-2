#!/usr/bin/env python3
"""
Complete deployment script with S3 storage
This script sets up S3 storage, uploads code, and creates a deployment
"""
import asyncio
import subprocess
import sys

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              cwd="/Users/arielberdugo/Documents/GE/gellc-prefect-2")
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

async def main():
    """Main deployment function"""
    
    print("🚀 GELLC Prefect S3 Deployment Pipeline")
    print("=" * 60)
    print("This script will:")
    print("1. Set up S3 storage for code")
    print("2. Upload your code to S3")
    print("3. Create a Prefect deployment with S3 storage")
    print("4. Test the deployment")
    print()
    
    input("Press Enter to continue...")
    
    # Step 1: Setup S3 storage
    if not run_script("setup_s3_storage.py", "Setting up S3 storage"):
        print("❌ Failed to setup S3 storage. Exiting.")
        return
    
    # Step 2: Upload code to S3
    if not run_script("upload_code_to_s3.py", "Uploading code to S3"):
        print("❌ Failed to upload code to S3. Exiting.")
        return
    
    # Step 3: Create deployment
    if not run_script("create_s3_deployment.py", "Creating S3 deployment"):
        print("❌ Failed to create deployment. Exiting.")
        return
    
    # Step 4: Test deployment (optional)
    print(f"\n{'='*60}")
    print("🎉 Deployment Setup Complete!")
    print(f"{'='*60}")
    
    test_choice = input("\nWould you like to test the deployment now? (y/n): ").lower()
    
    if test_choice in ['y', 'yes']:
        run_script("test_s3_deployment.py", "Testing S3 deployment")
    
    print(f"\n🎉 S3 Deployment Pipeline Complete!")
    print("=" * 50)
    print("📊 Summary:")
    print("✅ S3 bucket created and configured")
    print("✅ Code packaged and uploaded to S3")
    print("✅ Prefect deployment created with S3 storage")
    print()
    print("🔧 Next Steps:")
    print("1. Start a worker (if not running):")
    print("   prefect worker start --pool gellc-ecs-pool")
    print()
    print("2. Run your deployment:")
    print("   prefect deployment run 'my-first-flow/my-first-flow-s3'")
    print()
    print("3. Monitor in Prefect Cloud:")
    print("   https://app.prefect.cloud/")
    print()
    print("4. Update code (when needed):")
    print("   python upload_code_to_s3.py")

if __name__ == "__main__":
    asyncio.run(main())
