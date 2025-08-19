from prefect.deployments import Deployment
from prefect.infrastructure import Process
from prefect_aws import S3Bucket
from simple_ecs_flow import hello_flow
import asyncio

# 1. Configure S3 storage
s3_storage = S3Bucket(
    bucket_name="gellc-prefect-flows",
    basepath="flows/"
)

# 2. Configure infrastructure with stream_output=True
process_infra = Process(stream_output=True)

# 3. Build the deployment
deployment = Deployment.build_from_flow(
    flow=hello_flow,
    name="hello-flow-stream-output",
    storage=s3_storage,
    entrypoint="simple_ecs_flow.py:hello_flow",
    work_pool_name="gellc-process-pool",
    infrastructure=process_infra
)

# 4. Apply deployment and trigger a run
async def main():
    deployment_id = await deployment.apply()
    print(f"✅ Deployment applied: {deployment_id}")
    from prefect import get_client
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(deployment_id=deployment_id)
        print(f"✅ Triggered flow run: {flow_run.id}")
        base_url = "https://app.prefect.cloud/account/ab61b83d-af98-4940-ac58-024d88160a03/workspace/e31cc9e9-de96-4558-acdc-1ded94493b8d"
        print(f"🔗 {base_url}/flow-runs/flow-run/{flow_run.id}")

if __name__ == "__main__":
    asyncio.run(main())
