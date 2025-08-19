# S3-Based Prefect Deployment Guide

This guide explains how to upload your code to S3 and use it in Prefect deployments, allowing your ECS tasks to download and execute the code from S3.

## Overview

The S3 deployment setup includes:
- 📦 **Code Packaging**: Automatically package your Python code into a zip file
- ☁️ **S3 Storage**: Upload code to S3 bucket for remote access
- 🚀 **Prefect Integration**: Create deployments that reference S3-stored code
- 🧪 **Testing**: Verify that your deployment works correctly

## Prerequisites

1. **AWS Credentials**: Configure AWS CLI with appropriate permissions
   ```bash
   aws configure
   ```

2. **Prefect Cloud**: Connected to Prefect Cloud
   ```bash
   prefect cloud login
   ```

3. **Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Option 1: All-in-One Script
Run the complete deployment pipeline:
```bash
python deploy_with_s3.py
```

### Option 2: Step-by-Step

1. **Setup S3 Storage**
   ```bash
   python setup_s3_storage.py
   ```
   - Creates S3 bucket `gellc-prefect-code-storage`
   - Sets up Prefect S3 storage block
   - Configures permissions

2. **Upload Code to S3**
   ```bash
   python upload_code_to_s3.py
   ```
   - Packages your code into a zip file
   - Uploads to S3 bucket
   - Verifies upload

3. **Create Deployment**
   ```bash
   python create_s3_deployment.py
   ```
   - Creates Prefect deployment with S3 storage
   - Links to your ECS work pool

4. **Test Deployment**
   ```bash
   python test_s3_deployment.py
   ```
   - Runs a test flow execution
   - Monitors execution status

## File Structure

```
gellc-prefect-2/
├── setup_s3_storage.py      # Setup S3 bucket and Prefect storage block
├── upload_code_to_s3.py     # Package and upload code to S3
├── create_s3_deployment.py  # Create deployment with S3 storage
├── test_s3_deployment.py    # Test the S3 deployment
├── deploy_with_s3.py        # All-in-one deployment script
├── my_prefect_flow.py       # Your main flow code
├── requirements.txt         # Updated with S3 dependencies
└── src/                     # Additional source code (included in package)
```

## Configuration

### S3 Configuration
- **Bucket Name**: `gellc-prefect-code-storage`
- **Region**: `us-east-1`
- **Prefix**: `flows/`
- **Storage Block**: `gellc-s3-storage`

### ECS Configuration
- **Work Pool**: `gellc-ecs-pool`
- **Cluster**: `gellc-prefect-cluster`
- **Task Role**: `ecsTaskExecutionRole`

## How It Works

1. **Code Packaging**: The scripts automatically package your code files into a zip archive
2. **S3 Upload**: The zip file is uploaded to your S3 bucket
3. **Deployment Creation**: Prefect deployment is configured to use S3 storage
4. **Runtime Execution**: When a flow runs:
   - ECS task starts
   - Downloads code from S3
   - Extracts and executes your flow

## Included Files

The upload script automatically includes:
- `my_prefect_flow.py` - Main flow file
- `requirements.txt` - Dependencies
- `test_basic_flow.py` - Test flows
- `src/` directory - All source code

Excluded files:
- `__pycache__`, `*.pyc` - Python cache files
- `.git`, `.DS_Store` - System files
- `*.log`, `venv` - Temporary files

## Updating Code

When you modify your code:

1. **Upload new version**:
   ```bash
   python upload_code_to_s3.py
   ```

2. **The deployment automatically uses the latest code** from S3

## Troubleshooting

### Common Issues

1. **AWS Permissions Error**
   - Ensure your AWS credentials have S3 and ECS permissions
   - Check that the ECS task role can access the S3 bucket

2. **S3 Storage Block Not Found**
   - Run `python setup_s3_storage.py` first
   - Verify Prefect Cloud connection

3. **Deployment Not Found**
   - Check deployment name in Prefect Cloud
   - Ensure work pool `gellc-ecs-pool` exists

4. **Flow Execution Fails**
   - Check ECS task logs
   - Verify S3 download permissions
   - Ensure all dependencies are in requirements.txt

### Verification Commands

```bash
# Check S3 bucket contents
aws s3 ls s3://gellc-prefect-code-storage/flows/

# List Prefect deployments
prefect deployment ls

# Check work pools
prefect work-pool ls

# View flow runs
prefect flow-run ls --limit 5
```

## Benefits of S3 Storage

✅ **Version Control**: Each upload creates a new version in S3
✅ **Scalability**: Multiple ECS tasks can download the same code
✅ **Reliability**: S3 provides high availability and durability
✅ **Cost Effective**: Pay only for storage used
✅ **Integration**: Works seamlessly with AWS ECS

## Next Steps

After successful deployment:

1. **Start Workers**: Ensure ECS workers are running
   ```bash
   prefect worker start --pool gellc-ecs-pool
   ```

2. **Schedule Flows**: Set up schedules in Prefect Cloud

3. **Monitor**: Use Prefect Cloud dashboard to monitor executions

4. **Scale**: Add more workers as needed for higher throughput

## Support

For issues with this deployment setup:
1. Check the troubleshooting section above
2. Review ECS task logs in AWS CloudWatch
3. Check Prefect Cloud flow run logs
4. Verify AWS permissions and network connectivity
