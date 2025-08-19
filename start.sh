#!/bin/bash

# Prefect Container Startup Script

echo "🚀 Starting Prefect container..."
echo "Mode: ${PREFECT_MODE:-flow}"

case "${PREFECT_MODE:-flow}" in
    "worker")
        echo "📋 Starting as Prefect worker..."
        echo "Work Pool: ${PREFECT_WORK_POOL:-default}"
        prefect worker start --pool "${PREFECT_WORK_POOL:-default}" --type process
        ;;
    "flow")
        echo "🔄 Running flow directly..."
        python my_prefect_flow.py
        echo "✅ Flow completed, keeping container alive..."
        # Keep container alive for debugging/monitoring
        tail -f /dev/null
        ;;
    "server")
        echo "🏗️ Starting Prefect server..."
        prefect server start --host 0.0.0.0
        ;;
    *)
        echo "❌ Unknown mode: ${PREFECT_MODE}"
        echo "Valid modes: worker, flow, server"
        exit 1
        ;;
esac
