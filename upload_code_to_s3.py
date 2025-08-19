#!/usr/bin/env python3
"""
Upload code to S3 for Prefect deployments
"""
import asyncio
import os
import tempfile
import zipfile
from pathlib import Path
from prefect.filesystems import S3
import boto3

# Configuration
BUCKET_NAME = "gellc-prefect-code-storage"
BUCKET_PREFIX = "flows/"
AWS_REGION = "us-east-1"

# Files to include in the code package
INCLUDE_FILES = [
    "my_prefect_flow.py",
    "requirements.txt",
    "test_basic_flow.py",
    "src/",  # Include the entire src directory
]

# Files to exclude
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".git",
    ".DS_Store",
    "*.log",
    "venv",
    ".env"
]

def should_exclude(file_path):
    """Check if file should be excluded"""
    path_str = str(file_path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str or path_str.endswith(pattern.replace("*", "")):
            return True
    return False

def create_code_package():
    """Create a zip package of the code"""
    
    print("📦 Creating code package...")
    
    # Create temporary zip file
    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    temp_zip.close()
    
    base_path = Path("/Users/arielberdugo/Documents/GE/gellc-prefect-2")
    
    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file_pattern in INCLUDE_FILES:
            file_path = base_path / file_pattern
            
            if file_path.is_file():
                if not should_exclude(file_path):
                    arcname = file_path.name
                    zipf.write(file_path, arcname)
                    print(f"  ✅ Added file: {arcname}")
            
            elif file_path.is_dir():
                # Add directory contents recursively
                for root, dirs, files in os.walk(file_path):
                    # Remove excluded directories
                    dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
                    
                    for file in files:
                        file_full_path = Path(root) / file
                        if not should_exclude(file_full_path):
                            # Calculate relative path from base
                            rel_path = file_full_path.relative_to(base_path)
                            zipf.write(file_full_path, str(rel_path))
                            print(f"  ✅ Added file: {rel_path}")
    
    print(f"📦 Code package created: {temp_zip.name}")
    return temp_zip.name

async def upload_to_s3(zip_path):
    """Upload code package to S3"""
    
    print(f"☁️  Uploading to S3...")
    
    try:
        # Load S3 block
        s3_block = await S3.load("gellc-s3-storage")
        
        # Read zip file
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        # Upload to S3
        s3_key = "code.zip"
        await s3_block.write_path(s3_key, zip_content)
        
        s3_url = f"s3://{BUCKET_NAME}/{BUCKET_PREFIX}{s3_key}"
        print(f"✅ Code uploaded to: {s3_url}")
        
        return s3_url
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def verify_upload():
    """Verify the upload using boto3"""
    
    print("🔍 Verifying upload...")
    
    try:
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        
        # Check if object exists
        response = s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=f"{BUCKET_PREFIX}code.zip"
        )
        
        size_mb = response['ContentLength'] / (1024 * 1024)
        print(f"✅ Upload verified - Size: {size_mb:.2f} MB")
        print(f"✅ Last Modified: {response['LastModified']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def cleanup(zip_path):
    """Clean up temporary files"""
    try:
        os.unlink(zip_path)
        print("🧹 Cleaned up temporary files")
    except:
        pass

async def main():
    """Main upload function"""
    
    print("🚀 Uploading code to S3 for Prefect deployments")
    print("=" * 60)
    
    # Check if S3 block exists
    try:
        await S3.load("gellc-s3-storage")
        print("✅ S3 storage block found")
    except Exception as e:
        print(f"❌ S3 storage block not found: {e}")
        print("Please run: python setup_s3_storage.py")
        return
    
    # Create code package
    zip_path = create_code_package()
    
    try:
        # Upload to S3
        s3_url = await upload_to_s3(zip_path)
        
        if s3_url:
            # Verify upload
            if verify_upload():
                print("\n🎉 Code Upload Complete!")
                print("=" * 40)
                print(f"📊 Details:")
                print(f"  S3 URL: {s3_url}")
                print(f"  Bucket: {BUCKET_NAME}")
                print(f"  Key: {BUCKET_PREFIX}code.zip")
                print()
                print("🔧 Next Steps:")
                print("1. Create deployment with S3 storage:")
                print("   python create_s3_deployment.py")
                print()
                print("2. Test the deployment:")
                print("   python test_s3_deployment.py")
            else:
                print("❌ Upload verification failed")
        else:
            print("❌ Upload failed")
    
    finally:
        # Cleanup
        cleanup(zip_path)

if __name__ == "__main__":
    asyncio.run(main())
