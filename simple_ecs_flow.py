from prefect import flow, task, get_run_logger

@task
def hello_task(name: str = "World"):
    """Simple hello task"""
    logger = get_run_logger()
    message = f"Hello {name} from ECS!"
    logger.info(message)
    logger.info("✅ Running on ECS infrastructure!")
    return message

@flow
def hello_flow(name: str = "World"):
    """Simple hello flow"""
    logger = get_run_logger()
    logger.info(f"🚀 Starting flow for: {name}")
    result = hello_task(name)
    logger.info(f"📊 Result: {result}")
    return result

if __name__ == "__main__":
    hello_flow.serve(
        name="visible-ecs-deployment",
        tags=["visible", "ecs", "test"],
        parameters={"name": "ECS Test"}
    )
