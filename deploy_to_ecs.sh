#!/bin/bash

# GELLC Prefect ECS Deployment Script
set -e

echo "🚀 Deploying GELLC Prefect to ECS"
echo "================================="

# Variables
AWS_ACCOUNT_ID="576671272815"
AWS_REGION="us-east-1"
ECR_REPO="gellc-prefect"
CLUSTER_NAME="gellc-prefect-cluster"
SERVICE_NAME="gellc-prefect-service"
WORK_POOL_NAME="gellc-ecs-pool"

echo "📋 Configuration:"
echo "  AWS Account: $AWS_ACCOUNT_ID"
echo "  Region: $AWS_REGION"
echo "  ECR Repository: $ECR_REPO"
echo "  ECS Cluster: $CLUSTER_NAME"
echo "  Service: $SERVICE_NAME"
echo ""

# Step 1: Build and push Docker image
echo "📦 Building and pushing Docker image..."
docker build -t $ECR_REPO:latest .

# Tag for ECR
docker tag $ECR_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

echo "✅ Docker image pushed to ECR"

# Step 2: Create Prefect work pool
echo "🔧 Setting up Prefect work pool..."

# Check if work pool exists, create if it doesn't
if ! prefect work-pool ls | grep -q "$WORK_POOL_NAME"; then
    echo "Creating ECS work pool: $WORK_POOL_NAME"
    prefect work-pool create $WORK_POOL_NAME --type ecs
else
    echo "Work pool $WORK_POOL_NAME already exists"
fi

echo "✅ Prefect work pool ready"

# Step 3: Deploy flows
echo "🚢 Deploying Prefect flows..."
prefect deploy --all

echo "✅ Flows deployed"

# Step 4: Show status
echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo "📊 Infrastructure Status:"
echo "  ECS Cluster: $CLUSTER_NAME"
echo "  ECS Service: $SERVICE_NAME" 
echo "  ECR Image: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest"
echo "  Work Pool: $WORK_POOL_NAME"
echo ""
echo "🔧 Next Steps:"
echo "1. Start Prefect server (if not running):"
echo "   prefect server start"
echo ""
echo "2. Start a worker to handle flows:"
echo "   prefect worker start --pool $WORK_POOL_NAME"
echo ""
echo "3. Run a flow:"
echo "   prefect deployment run 'my-first-flow/my-first-flow-ecs'"
echo ""
echo "4. Monitor in Prefect UI:"
echo "   http://localhost:4200"
echo ""
echo "5. Check ECS service status:"
echo "   aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME"
