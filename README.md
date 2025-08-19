# GELLC Prefect ECS Deployment

This project demonstrates how to deploy Prefect flows to AWS ECS using Fargate.

## Architecture

- **Docker Container**: Prefect application containerized with Python 3.9
- **ECR Repository**: `576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect`
- **ECS Cluster**: `gellc-prefect-cluster`
- **ECS Service**: `gellc-prefect-service`
- **Task Definition**: `gellc-prefect-task`
- **Network**: VPC `vpc-b355c1c9` with public subnets
- **Security Group**: `sg-07df2040c0081cac5` (allows traffic on port 8080)

## Deployed Infrastructure

✅ **ECR Repository**: `gellc-prefect` - stores Docker images  
✅ **ECS Cluster**: `gellc-prefect-cluster` - container orchestration  
✅ **ECS Task Definition**: `gellc-prefect-task:1` - container specifications  
✅ **ECS Service**: `gellc-prefect-service` - manages running tasks  
✅ **Security Group**: `sg-07df2040c0081cac5` - network security  
✅ **CloudWatch Logs**: `/ecs/gellc-prefect-task` - container logging  

### Current Status
- **Public IP**: `44.202.220.25`
- **Container Status**: Running on ECS Fargate
- **Resource Allocation**: 256 CPU, 512 MB memory

## Quick Start

### 1. Prerequisites
```bash
# AWS CLI configured
aws configure

# Docker installed and running
docker --version

# Prefect installed
pip install prefect
```

### 2. Deploy Everything
```bash
# One-command deployment
./deploy_to_ecs.sh
```

### 3. Manual Deployment Steps

#### Build and Push Docker Image
```bash
# Build image
docker build -t gellc-prefect:latest .

# Tag for ECR
docker tag gellc-prefect:latest 576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 576671272815.dkr.ecr.us-east-1.amazonaws.com

# Push to ECR
docker push 576671272815.dkr.ecr.us-east-1.amazonaws.com/gellc-prefect:latest
```

#### Setup Prefect
```bash
# Create ECS work pool
prefect work-pool create gellc-ecs-pool --type ecs

# Deploy flows
prefect deploy --all
```

## Running Flows

### 1. Start Prefect Server
```bash
prefect server start
```

### 2. Start Worker
```bash
# In another terminal
prefect worker start --pool gellc-ecs-pool
```

### 3. Run Deployment
```bash
# Trigger flow run
prefect deployment run 'my-first-flow/my-first-flow-ecs'

# Or schedule runs
prefect deployment run 'my-first-flow/my-first-flow-ecs' --param name="ECS"
```

### 4. Monitor
- **Prefect UI**: http://localhost:4200
- **AWS Console**: ECS → Clusters → gellc-prefect-cluster
- **CloudWatch Logs**: `/ecs/gellc-prefect-task`

## Configuration Files

### Core Files
- `Dockerfile` - Container definition
- `requirements.txt` - Python dependencies
- `my_prefect_flow.py` - Sample Prefect flow
- `prefect.yaml` - Deployment configuration

### ECS Configuration
- `ecs-task-definition.json` - ECS task definition
- `trust-policy.json` - IAM role policy

### Deployment Scripts
- `deploy_to_ecs.sh` - One-command deployment
- `setup_prefect_ecs.py` - Prefect infrastructure setup
- `prefect_deployment.py` - Legacy deployment method

## Infrastructure Details

### AWS Resources Created
```
├── ECR Repository: gellc-prefect
├── ECS Cluster: gellc-prefect-cluster
├── ECS Service: gellc-prefect-service
├── ECS Task Definition: gellc-prefect-task:1
├── Security Group: sg-07df2040c0081cac5
├── CloudWatch Log Group: /ecs/gellc-prefect-task
└── IAM Role: ecsTaskExecutionRole
```

### Network Configuration
- **VPC**: `vpc-b355c1c9` (default VPC)
- **Subnets**: `subnet-74ebae28`, `subnet-30f38b57`
- **Security Group**: `sg-07df2040c0081cac5`
- **Public IP**: Enabled for internet access

### Resource Specifications
- **CPU**: 256 units (0.25 vCPU)
- **Memory**: 512 MB
- **Launch Type**: Fargate (serverless)
- **Platform**: Linux

## Troubleshooting

### Check ECS Service Status
```bash
aws ecs describe-services \
  --cluster gellc-prefect-cluster \
  --services gellc-prefect-service
```

### View Container Logs
```bash
aws logs tail /ecs/gellc-prefect-task --follow
```

### Debug Task Issues
```bash
# List tasks
aws ecs list-tasks --cluster gellc-prefect-cluster

# Describe specific task
aws ecs describe-tasks \
  --cluster gellc-prefect-cluster \
  --tasks <task-id>
```

### Common Issues
1. **Task fails to start**: Check CloudWatch logs for container errors
2. **Network connectivity**: Verify security group allows necessary ports
3. **Image pull errors**: Ensure ECR authentication and image exists
4. **Permission issues**: Verify IAM roles have necessary policies

## Advanced Configuration

### Custom Environment Variables
Edit `ecs-task-definition.json` to add environment variables:
```json
"environment": [
  {"name": "PYTHONPATH", "value": "/app"},
  {"name": "PREFECT_API_URL", "value": "your-prefect-server-url"},
  {"name": "AWS_DEFAULT_REGION", "value": "us-east-1"}
]
```

### Scaling
```bash
# Scale service to 2 tasks
aws ecs update-service \
  --cluster gellc-prefect-cluster \
  --service gellc-prefect-service \
  --desired-count 2
```

### Monitoring
- Set up CloudWatch alarms for task health
- Enable Container Insights for detailed metrics
- Configure log retention policies

## Cleanup

To remove all resources:
```bash
# Delete ECS service
aws ecs update-service --cluster gellc-prefect-cluster --service gellc-prefect-service --desired-count 0
aws ecs delete-service --cluster gellc-prefect-cluster --service gellc-prefect-service

# Delete cluster
aws ecs delete-cluster --cluster gellc-prefect-cluster

# Delete ECR repository
aws ecr delete-repository --repository-name gellc-prefect --force

# Delete security group
aws ec2 delete-security-group --group-id sg-07df2040c0081cac5

# Delete log group
aws logs delete-log-group --log-group-name /ecs/gellc-prefect-task
```
