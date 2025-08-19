from prefect import flow, task

@task
def hello_task(name: str = "World"):
    """Simple hello task"""
    message = f"Hello {name} from ECS!"
    print(message)
    print("✅ Running on ECS infrastructure!")
    return message

@flow
def hello_flow(name: str = "World"):
    """Simple hello flow"""
    print(f"🚀 Starting flow for: {name}")
    result = hello_task(name)
    print(f"📊 Result: {result}")
    return result

if __name__ == "__main__":
    hello_flow.serve(
        name="visible-ecs-deployment",
        tags=["visible", "ecs", "test"],
        parameters={"name": "ECS Test"}
    )
